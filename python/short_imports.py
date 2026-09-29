"""Shorten parenthesized, multiline imports of names from a child module."""

from difflib import unified_diff
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
    path: Path
    write: bool = False


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


def main() -> None:
    options = tyro.cli(Options)
    original = options.path.read_text()
    changed = shorten_imports(original)
    if options.write:
        if changed != original:
            options.path.write_text(changed)
    else:
        print(
            ''.join(
                unified_diff(
                    original.splitlines(keepends=True),
                    changed.splitlines(keepends=True),
                    fromfile=str(options.path),
                    tofile=str(options.path),
                )
            ),
            end='',
        )


if __name__ == '__main__':
    main()
