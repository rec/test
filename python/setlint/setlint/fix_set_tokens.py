from .token_line import TokenLine
from .python_file import PythonFile
import token


def fix_set_tokens(pf: PythonFile) -> tuple[list[str], int]:
    lines = list(pf.lines)
    if not pf.set_tokens:
        return lines, 0

    for t in sorted(pf.set_tokens, reverse=True, key=lambda t: t.start):
        (start_line, start_col), (end_line, end_col) = t.start, t.end
        assert start_line == end_line
        line = lines[start_line - 1]
        assert line == t.line

        a, b, c = line[:start_col], line[start_col:end_col], line[end_col:]
        print(f"{a=}, {b=}, {c=}, {line=}")
        assert b == "set"
        lines[start_line - 1] = f"{a}OrderedSet{c}"

    count = _add_import(lines, pf.token_lines) + len(pf.set_tokens)
    return lines, count


def _add_import(lines: list[str], token_lines: list[TokenLine]) -> int:
    entries: dict[str, list[TokenLine]] = {"from": [], "comment": [], "import": []}
    for tl in token_lines:
        t = tl.tokens[0]
        if t.type == token.INDENT:
            break
        elif t.type == token.COMMENT:
            entries["comments"].append(tl)
        elif not (t.type == token.NAME and t.string in ("from", "import")):
            continue
        elif any(i.type == token.NAME and i.string == "OrderedSet" for i in tl.tokens):
            return 0
        else:
            entries[t.string].append(tl)

    if imps := entries["from"] or entries["import"] or entries["comment"]:
        insert_before = imps[-1].tokens[-1].start[0] + 1
    else:
        insert_before = 0
    lines.insert(insert_before, "from torch.utils._ordered_set import OrderedSet\n")
    return 1
