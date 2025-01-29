import os
import sys, token
from pathlib import Path
from tokenize import generate_tokens, TokenInfo
from typing import Iterator

def token_lines(tokens) -> list[list[TokenInfo]]:
    """Returns lists of TokenInfo segmented by token.NEWLINE"""
    token_lines: list[list[TokenInfo]] = [[]]

    for t in tokens:
        if t.type not in (token.COMMENT, token.ENDMARKER, token.NL):
            token_lines[-1].append(t)
            if t.type == token.NEWLINE:
                token_lines.append([])
    while token_lines and not token_lines[-1]:
        token_lines.pop()
    return token_lines


def join_lines(tokens):
    lineno = 0
    lines = []
    for t in tokens:
        if t.start[0] != lineno:
            lines.append(t.line.strip())
            lineno = t.start[0]
    return " ".join(" ".join(lines).split()).strip()


def list_imports(tokens) -> Iterator[str]:
    for tl in token_lines(tokens):
        t = tl[0]
        if t.type == token.NAME and t.string in ("from", "import"):
            yield join_lines(tl)


def split_import(line):
    if "*" in line:
        return []

    fr, _, im = line.partition('import')
    im = im.replace("(", "").replace(")", "")
    parts = [ps.split()[0] for p in im.split(",") if (ps := p.strip())]

    if not fr:
        return parts
    fr, _, rest = fr.strip().partition("from ")
    assert not fr
    return [f"{rest}.{p}" for p in parts]


def all_python_files(path: Path, python_root=None):
    python_root = python_root or Path(".")
    if path.suffix == ".py":
        paths = [path]
    else:
        paths  = sorted(path.glob("**/*.py"))
    for f in paths:
        f = f.relative_to(python_root)
        module_path = [i.name for i in reversed(f.parents)][1:]
        if any('.' in i for i in module_path):
            continue

        with f.open() as fp:
            tokens = list(generate_tokens(fp.readline))

        for imp in list_imports(tokens):
            for i in split_import(imp):
                simp = i.lstrip(".")
                if diff := len(i) - len(simp):
                    i = ".".join(module_path[:(1 - diff) or None] + [simp])
                print(f, i)


if __name__ == '__main__':
    for i in sys.argv[1:]:
        all_python_files(Path(i))
