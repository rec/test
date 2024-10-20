from .python_file import PythonFile
from token import COMMENT, INDENT, NAME

IMPORT_LINE = "from torch.utils._ordered_set import OrderedSet\n"


def fix_set_tokens(pf: PythonFile) -> None:
    _fix_tokens(pf)
    _add_import(pf)


def _fix_tokens(pf: PythonFile) -> None:
    for t in sorted(pf.set_tokens, reverse=True, key=lambda t: t.start):
        (start_line, start_col), (end_line, end_col) = t.start, t.end
        assert start_line == end_line
        line = pf.lines[start_line - 1]

        a, b, c = line[:start_col], line[start_col:end_col], line[end_col:]
        assert b in ("set", "Set")
        pf.lines[start_line - 1] = f"{a}OrderedSet{c}"


def _add_import(pf: PythonFile) -> None:
    if not pf.set_tokens:
        return

    froms, comments, imports = [], [], []

    for tl in pf.token_lines:
        t = tl.tokens[0]
        if t.type == INDENT:
            break
        elif t.type == COMMENT:
            comments.append(tl)
        elif t.type == NAME and t.string in ("from", "import"):
            if any(i.type == NAME and i.string == "OrderedSet" for i in tl.tokens):
                return
            elif t.string == "from":
                froms.append(tl)
            else:
                imports.append(tl)

    if section := froms or imports or comments:
        insert_before = section[-1].tokens[-1].start[0] + 1
    else:
        insert_before = 0
    pf.lines.insert(insert_before, IMPORT_LINE)
