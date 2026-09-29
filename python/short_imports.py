"""Shorten parenthesized, multiline imports in Git projects or Python files."""

import re
import shlex
import subprocess
import sys
from pathlib import Path

import libcst as cst
import tyro
from libcst.helpers import get_full_name_for_node
from libcst.metadata import (
    ImportAssignment,
    MetadataWrapper,
    PositionProvider,
    ScopeProvider,
)
from pydantic import BaseModel


class Options(BaseModel, frozen=True):
    paths: tyro.conf.Positional[list[Path]]
    useful: bool = True
    stash: bool = False


class ImportComments(cst.CSTVisitor):
    def __init__(self) -> None:
        self.comments: list[cst.Comment] = []

    def visit_Comment(self, node: cst.Comment) -> None:
        self.comments.append(node)


class ShortenImports(cst.CSTTransformer):
    def __init__(
        self,
        imports: dict[cst.ImportFrom, tuple[str | None, str]],
        references: dict[cst.Name, str],
    ) -> None:
        self.imports = imports
        self.references = references

    def leave_Name(
        self, original_node: cst.Name, updated_node: cst.Name
    ) -> cst.BaseExpression:
        if (name := self.references.get(original_node)) is None:
            return updated_node
        module, imported = name.rsplit('.', 1)
        return cst.Attribute(value=cst.Name(module), attr=cst.Name(imported))

    def leave_ImportFrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> cst.ImportFrom:
        if (target := self.imports.get(original_node)) is None:
            return updated_node
        parent, module = target
        return updated_node.with_changes(
            module=cst.parse_expression(parent) if parent else None,
            names=(cst.ImportAlias(name=cst.Name(module)),),
            lpar=None,
            rpar=None,
        )

    def leave_SimpleStatementLine(
        self,
        original_node: cst.SimpleStatementLine,
        updated_node: cst.SimpleStatementLine,
    ) -> cst.SimpleStatementLine:
        if (
            len(original_node.body) != 1
            or (import_node := original_node.body[0]) not in self.imports
        ):
            return updated_node
        comments = ImportComments()
        import_node.visit(comments)
        return updated_node.with_changes(
            leading_lines=(
                *updated_node.leading_lines,
                *(cst.EmptyLine(comment=comment) for comment in comments.comments),
            )
        )


def shorten_imports(source: str) -> str:
    wrapper = MetadataWrapper(cst.parse_module(source))
    positions = wrapper.resolve(PositionProvider)
    scopes = set(wrapper.resolve(ScopeProvider).values())
    candidates: dict[cst.ImportFrom, tuple[str | None, str]] = {}
    modules: dict[str, set[cst.ImportFrom]] = {}
    for scope in scopes:
        for assignment in scope.assignments:
            node = assignment.node
            if not isinstance(assignment, ImportAssignment) or not isinstance(
                node, cst.ImportFrom
            ):
                continue
            if (
                node.lpar is None
                or positions[node].start.line == positions[node].end.line
                or node.module is None
                or isinstance(node.names, cst.ImportStar)
            ):
                continue
            if (name := get_full_name_for_node(node.module)) is not None:
                parent, _, module = name.rpartition('.')
                if not parent and not node.relative:
                    continue
                candidates[node] = (parent or None, module)
                modules.setdefault(module, set()).add(node)
    imports: dict[cst.ImportFrom, tuple[str | None, str]] = {}
    references: dict[cst.Name, str] = {}

    for scope in scopes:
        for assignment in scope.assignments:
            node = assignment.node
            if not isinstance(assignment, ImportAssignment) or not isinstance(
                node, cst.ImportFrom
            ):
                continue
            if (target := candidates.get(node)) is None or node in imports:
                continue
            parent, module = target
            if module in scope or len(modules[module]) > 1:
                continue

            imported = {
                alias.evaluated_alias or alias.evaluated_name: alias.evaluated_name
                for alias in node.names
            }
            bindings = {
                a.name: a
                for a in scope.assignments
                if isinstance(a, ImportAssignment) and a.node is node
            }
            if imported.keys() != bindings.keys():
                continue
            if any(
                not isinstance(access.node, cst.Name)
                or set(access.referents) != {binding}
                or module in access.scope
                for binding in bindings.values()
                for access in binding.references
            ):
                continue

            imports[node] = (parent, module)
            for local_name, binding in bindings.items():
                for access in binding.references:
                    if isinstance(access.node, cst.Name):
                        references[access.node] = f'{module}.{imported[local_name]}'

    return wrapper.module.visit(ShortenImports(imports, references)).code


def shorten_file(path: Path, originals: dict[Path, bytes]) -> None:
    original = path.read_bytes()
    originals.setdefault(path, original)
    source = original.decode()
    changed = shorten_imports(source)
    if changed != source:
        path.write_text(changed)


def run_projects(paths: list[Path], useful: bool = True, stash: bool = False) -> None:
    if not paths:
        sys.exit('At least one project or Python file path is required')

    direct_files: list[Path] = []
    project_paths: list[Path] = []
    workspaces: list[Path] = []
    projects: dict[Path, list[str]] = {}
    untracked_before: dict[Path, bytes] = {}
    for path in paths:
        if path.is_symlink() and not path.is_dir():
            sys.exit(f'Symlinks are not supported: {path}')
        target = path.resolve()
        if target.is_file():
            if target.suffix != '.py':
                sys.exit(f'Not a Python file: {target}')
            if target not in direct_files:
                direct_files.append(target)
            if stash:
                try:
                    root = Path(
                        _git_output(target.parent, 'rev-parse', '--show-toplevel')
                        .decode()
                        .strip()
                    )
                except RuntimeError:
                    pass
                else:
                    if root not in workspaces:
                        workspaces.append(root)
            continue
        if not target.is_dir():
            sys.exit(f'Not a project directory or Python file: {target}')
        try:
            root = Path(
                _git_output(target, 'rev-parse', '--show-toplevel').decode().strip()
            )
            if root != target:
                sys.exit(f'Pass the Git project root, not a subdirectory: {target}')
        except (OSError, RuntimeError) as error:
            sys.exit(str(error))
        if root not in project_paths:
            project_paths.append(root)
        if stash and root not in workspaces:
            workspaces.append(root)

    if stash:
        for project in workspaces:
            if _git_output(project, 'status', '--porcelain', '-uno', '-z'):
                subprocess.run(['git', 'stash'], cwd=project, check=True)

    for project in project_paths:
        try:
            if _git_output(project, 'status', '--porcelain', '-uno', '-z'):
                sys.exit(f'Project has existing changes: {project}')
            untracked_before[project] = _git_output(
                project, 'ls-files', '--others', '--exclude-standard', '-z'
            )
            files = [
                p.decode('utf-8', errors='surrogateescape')
                for p in _git_output(project, 'ls-files', '-z', '--', '*.py').split(
                    b'\0'
                )
                if p
            ]
        except (OSError, RuntimeError) as error:
            sys.exit(str(error))
        if not files:
            sys.exit(f'No tracked Python files: {project}')
        if any(
            not (project / p).is_file() or (project / p).is_symlink() for p in files
        ):
            sys.exit(f'Tracked Python file is missing or a symlink: {project}')
        projects[project] = files

    failures: list[str] = []
    originals: dict[Path, bytes] = {}
    for path in direct_files:
        try:
            shorten_file(path, originals)
        except (OSError, UnicodeError, cst.ParserSyntaxError) as error:
            failures.append(f'{path}: {error}')
    for project, files in projects.items():
        for name in files:
            path = project / name
            try:
                shorten_file(path, originals)
            except (OSError, UnicodeError, cst.ParserSyntaxError) as error:
                failures.append(f'{path}: {error}')
        failures.extend(run_checks(project, files))

    if useful:
        for path, original in originals.items():
            try:
                current = path.read_bytes()
                if current != original and len(current.splitlines()) >= len(
                    original.splitlines()
                ):
                    path.write_bytes(original)
            except OSError as error:
                failures.append(f'{path}: {error}')

    if failures:
        sys.exit('No commits made. Failures:\n' + '\n'.join(failures))

    for project in projects:
        changed = [
            p.decode('utf-8', errors='surrogateescape')
            for p in _git_output(project, 'diff', '--name-only', '-z').split(b'\0')
            if p
        ]
        untracked = _git_output(
            project, 'ls-files', '--others', '--exclude-standard', '-z'
        )
        staged = _git_output(project, 'diff', '--cached', '--name-only', '-z')
        if (
            untracked != untracked_before[project]
            or staged
            or any(
                p not in projects[project] or not (project / p).is_file()
                for p in changed
            )
        ):
            failures.append(f'{project}: checks created unexpected files or changes')
        projects[project] = changed

    if failures:
        sys.exit('No commits made. Failures:\n' + '\n'.join(failures))

    for project, changed in projects.items():
        if not changed:
            print(f'{project}: no changes')
            continue
        subprocess.run(['git', 'add', '--', *changed], cwd=project, check=True)
        subprocess.run(
            ['git', 'commit', '-m', 'Shortened imports'], cwd=project, check=True
        )


def run_checks(project: Path, files: list[str]) -> list[str]:
    bin_dir = project / '.venv/bin'
    failures: list[str] = []
    try:
        version = _python_version(project)
    except (OSError, RuntimeError, ValueError) as error:
        failures.append(f'{project}: pyupgrade: {error}')
        version = None

    checks = []
    if version is not None:
        checks.append(
            ('pyupgrade', [bin_dir / 'pyupgrade', f'--py{version}-plus', *files])
        )
    checks.extend(
        [
            ('ruff format', [bin_dir / 'ruff', 'format', *files]),
            (
                'ruff check',
                [bin_dir / 'ruff', 'check', '--fix', '--select', 'B,E,F,I', *files],
            ),
            ('pytest', [bin_dir / 'pytest']),
            ('git diff --check', ['git', 'diff', '--check']),
        ]
    )
    for label, command in checks:
        print(f'{project}: {shlex.join(str(a) for a in command)}', flush=True)
        try:
            result = subprocess.run(command, cwd=project, check=False)
        except OSError as error:
            failures.append(f'{project}: {label}: {error}')
            continue
        if result.returncode:
            failures.append(f'{project}: {label} exited {result.returncode}')
    return failures


def main() -> None:
    options = tyro.cli(Options)
    run_projects(options.paths, options.useful, options.stash)


def _git_output(project: Path, *args: str) -> bytes:
    result = subprocess.run(
        ['git', *args], cwd=project, capture_output=True, check=False
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace').strip())
    return result.stdout


def _python_version(project: Path) -> str:
    version_file = project / '.python-version'
    if version_file.is_file():
        version = version_file.read_text().strip()
    else:
        result = subprocess.run(
            [project / '.venv/bin/python', '--version'],
            cwd=project,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or 'venv Python failed')
        version = result.stdout.removeprefix('Python ').strip()
    if (match := re.fullmatch(r'(\d+)\.(\d+)(?:\.\d+)?', version)) is None:
        raise ValueError(f'Invalid Python version: {version}')
    return ''.join(match.groups())


if __name__ == '__main__':
    main()
