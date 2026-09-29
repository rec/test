import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import tyro
from short_imports import Options, run_checks, run_projects, shorten_imports


def test_paths_are_positional_arguments() -> None:
    options = tyro.cli(Options, args=['/tmp/first', '/tmp/second'])
    assert options.paths == [Path('/tmp/first'), Path('/tmp/second')]
    assert options.useful is True
    assert tyro.cli(Options, args=['/tmp/first', '--no-useful']).useful is False


class ShortImportsTest(unittest.TestCase):
    def test_rewrites_multiline_import_and_its_references(self) -> None:
        source = """from ..one.two import (
    a,
    b as renamed,
    # More imports
)

result = a(renamed)
"""
        expected = """# More imports
from ..one import two

result = two.a(two.b)
"""
        self.assertEqual(shorten_imports(source), expected)

    def test_leaves_other_imports_and_shadowed_names_alone(self) -> None:
        source = """from one.two import (a, b)
from one.two import a
from one.two import (
    c,
)

def use(c):
    return c

result = c
"""
        expected = """from one.two import (a, b)
from one.two import a
from one import two

def use(c):
    return c

result = two.c
"""
        self.assertEqual(shorten_imports(source), expected)

    def test_skips_import_when_new_module_name_conflicts(self) -> None:
        source = """two = object()
from one.two import (
    a,
)
result = a
"""
        self.assertEqual(shorten_imports(source), source)

    def test_skips_import_when_module_name_is_shadowed_at_reference(self) -> None:
        source = """from one.two import (
    a,
)

def use(two):
    return a
"""
        self.assertEqual(shorten_imports(source), source)

    def test_skips_imports_that_would_bind_the_same_module_name(self) -> None:
        source = """from one.two import (
    a,
)
from other.two import (
    b,
)
result = a(b)
"""
        self.assertEqual(shorten_imports(source), source)

    def test_skips_same_module_name_across_nested_scopes(self) -> None:
        source = """from one.two import (
    a,
)

def use():
    from other.two import (
        b,
    )
    return a(b)
"""
        self.assertEqual(shorten_imports(source), source)


class ProjectTest(unittest.TestCase):
    def test_changes_tracked_and_untracked_files_without_checks_or_commit(
        self,
    ) -> None:
        with TemporaryDirectory() as directory:
            project = Path(directory)
            self._init_project(project)
            (project / 'package').mkdir()
            selected = project / 'package' / 'selected.py'
            tracked = project / 'tracked.py'
            other = project / 'other.py'
            source = 'from one.two import (\n    a,\n)\nresult = a\n'
            selected.write_text(source)
            tracked.write_text(source)
            other.write_text(source)
            self._git(project, 'add', 'tracked.py', 'other.py')
            self._git(project, 'commit', '-qm', 'Initial')

            with patch('short_imports.run_checks', return_value=[]) as checks:
                run_projects([selected, tracked])

            checks.assert_not_called()
            for path in (selected, tracked):
                self.assertEqual(
                    path.read_text(), 'from one import two\nresult = two.a\n'
                )
            self.assertEqual(other.read_text(), source)
            self.assertEqual(self._git(project, 'log', '-1', '--format=%s'), 'Initial')

    def test_changes_python_file_outside_git(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'standalone.py'
            path.write_text('from one.two import (\n    a,\n)\nresult = a\n')

            run_projects([path])

            self.assertEqual(path.read_text(), 'from one import two\nresult = two.a\n')

    def test_restores_standalone_file_when_line_count_does_not_decrease(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'standalone.py'
            original = b'result = a\r\n'
            path.write_bytes(original)

            with patch(
                'short_imports.shorten_imports', return_value='result = two.a\n'
            ):
                run_projects([path])

            self.assertEqual(path.read_bytes(), original)

    def test_commits_only_files_that_remain_shorter_after_checks(self) -> None:
        with TemporaryDirectory() as directory:
            project = Path(directory)
            self._init_project(project)
            source = 'from one.two import (\n    a,\n)\nresult = a\n'
            for name in ('useful.py', 'not_useful.py'):
                (project / name).write_text(source)
            self._git(project, 'add', 'useful.py', 'not_useful.py')
            self._git(project, 'commit', '-qm', 'Initial')

            def add_lines(project: Path, files: list[str]) -> list[str]:
                path = project / 'not_useful.py'
                path.write_text(path.read_text() + 'padding = 1\npadding2 = 2\n')
                return []

            with patch('short_imports.run_checks', side_effect=add_lines):
                run_projects([project])

            self.assertEqual((project / 'not_useful.py').read_text(), source)
            self.assertEqual(
                (project / 'useful.py').read_text(),
                'from one import two\nresult = two.a\n',
            )
            self.assertEqual(
                self._git(project, 'show', '--format=', '--name-only', 'HEAD'),
                'useful.py',
            )

    def test_no_useful_keeps_file_even_when_line_count_does_not_decrease(
        self,
    ) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'standalone.py'
            path.write_text('result = a\n')

            with patch(
                'short_imports.shorten_imports', return_value='result = two.a\n'
            ):
                run_projects([path], useful=False)

            self.assertEqual(path.read_text(), 'result = two.a\n')

    def test_project_argument_includes_all_files_after_file_argument(self) -> None:
        with TemporaryDirectory() as directory:
            project = Path(directory)
            self._init_project(project)
            source = 'from one.two import (\n    a,\n)\nresult = a\n'
            for name in ('first.py', 'second.py'):
                (project / name).write_text(source)
            self._git(project, 'add', 'first.py', 'second.py')
            self._git(project, 'commit', '-qm', 'Initial')

            with patch('short_imports.run_checks', return_value=[]) as checks:
                run_projects([project / 'first.py', project])

            checks.assert_called_once_with(project.resolve(), ['first.py', 'second.py'])
            for name in ('first.py', 'second.py'):
                self.assertEqual(
                    (project / name).read_text(),
                    'from one import two\nresult = two.a\n',
                )

    def test_commits_only_tracked_python_files_after_checks_pass(self) -> None:
        with TemporaryDirectory() as directory:
            project = Path(directory)
            self._init_project(project)
            (project / '.gitignore').write_text('ignored.py\n')
            (project / 'tracked.py').write_text(
                'from one.two import (\n    a,\n)\nresult = a\n'
            )
            (project / 'ignored.py').write_text(
                'from one.two import (\n    a,\n)\nresult = a\n'
            )
            self._git(project, 'add', '.gitignore', 'tracked.py')
            self._git(project, 'commit', '-qm', 'Initial')

            with patch('short_imports.run_checks', return_value=[]):
                run_projects([project])

            self.assertEqual(
                (project / 'tracked.py').read_text(),
                'from one import two\nresult = two.a\n',
            )
            self.assertIn('from one.two import', (project / 'ignored.py').read_text())
            self.assertEqual(
                self._git(project, 'log', '-1', '--format=%s'), 'Shortened imports'
            )

    def test_failed_checks_prevent_commits_in_all_projects(self) -> None:
        with TemporaryDirectory() as directory:
            projects = [Path(directory) / name for name in ('first', 'second')]
            for project in projects:
                project.mkdir()
                self._init_project(project)
                (project / 'tracked.py').write_text(
                    'from one.two import (\n    a,\n)\nresult = a\n'
                )
                self._git(project, 'add', 'tracked.py')
                self._git(project, 'commit', '-qm', 'Initial')

            with patch(
                'short_imports.run_checks', side_effect=[[], ['pytest exited 1']]
            ):
                with self.assertRaises(SystemExit):
                    run_projects(projects)

            for project in projects:
                self.assertEqual(
                    self._git(project, 'log', '-1', '--format=%s'), 'Initial'
                )
                self.assertIn(
                    'from one import two', (project / 'tracked.py').read_text()
                )

    def test_rejects_dirty_project_before_rewriting(self) -> None:
        with TemporaryDirectory() as directory:
            project = Path(directory)
            self._init_project(project)
            source = 'from one.two import (\n    a,\n)\nresult = a\n'
            (project / 'tracked.py').write_text(source)
            self._git(project, 'add', 'tracked.py')
            self._git(project, 'commit', '-qm', 'Initial')
            (project / 'untracked.txt').write_text('Existing user work\n')

            with self.assertRaises(SystemExit):
                run_projects([project])

            self.assertEqual((project / 'tracked.py').read_text(), source)
            self.assertEqual(self._git(project, 'log', '-1', '--format=%s'), 'Initial')

    def test_runs_every_check_after_a_failure(self) -> None:
        with TemporaryDirectory() as directory:
            project = Path(directory)
            (project / '.python-version').write_text('3.10\n')
            result = subprocess.CompletedProcess([], 1)
            with patch('short_imports.subprocess.run', return_value=result) as run:
                failures = run_checks(project, ['tracked.py'])

            self.assertEqual(run.call_count, 6)
            self.assertEqual(len(failures), 6)
            commands = [call.args[0] for call in run.call_args_list]
            self.assertIn('format', commands[1])
            self.assertIn('--fix', commands[2])
            self.assertIn('pytest', str(commands[3][0]))

    def _init_project(self, project: Path) -> None:
        self._git(project, 'init', '-q')
        self._git(project, 'config', 'user.name', 'Test')
        self._git(project, 'config', 'user.email', 'test@example.com')

    def _git(self, project: Path, *args: str) -> str:
        return subprocess.run(
            ['git', *args], cwd=project, capture_output=True, text=True, check=True
        ).stdout.strip()


if __name__ == '__main__':
    unittest.main()
