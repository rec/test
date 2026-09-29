import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import tyro
from short_imports import Options, run_checks, run_projects, shorten_imports


def test_projects_are_positional_arguments() -> None:
    options = tyro.cli(Options, args=['/tmp/first', '/tmp/second'])
    assert options.projects == [Path('/tmp/first'), Path('/tmp/second')]


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
