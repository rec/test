from .token_line import TokenLine
from .python_file import PythonFile
import token


def fix_tokens_using_set(token_lines: PythonFile) -> tuple[list[str], int]:
    if not (tokens := list(token_lines.tokens)):
        return [], 0

    # First replace all the instances of set with OrderedSet
    with open(token_lines.filename) as fp:
        contents = fp.readlines()

    tokens.sort(key=lambda t: t.start, reverse=True)
    for count, t in enumerate(tokens):
        (start_line, start_col), (end_line, end_col) = t.start, t.end
        assert start_line == end_line
        line = contents[start_line]

        a, b, c = line[:start_col], line[start_col:end_col], line[end_col:]
        assert b == "set"
        contents[start_line] = f"{a}OrderedSet{c}"

    if not any(_is_ordered_set_import(line) for line in contents):
        # Add the missing import and hope that ruff puts it in the right place
        _add_import(contents, token_lines.token_lines)
        count += 1

    return contents, count


def _is_ordered_set_import(line: str) -> bool:
    parts = [j for i in line.split() for j in i.split(".") if j]
    return (
        bool(parts)
        and parts[0] == "from"
        and parts[-1] == "OrderedSet"
        and "import" in parts
        and "utils" in parts
    )


def _add_import(contents: list[str], token_lines: list[TokenLine]):
    lines: dict[str, list[TokenLine]] = {}
    for tl in token_lines:
        t = tl.tokens[0]
        if t.type == token.NAME:
            lines.setdefault(t.string, []).append(tl)


"""
            lasts[tl[0].string] = tl
    froms = [tl for tl in tokens.token_lines if accept(tl, 'from')]
    """
