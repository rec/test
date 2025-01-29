import os
import sys, token
from tokenize import generate_tokens, TokenInfo
from typing import Iterator

"""
"import" module ["as" identifier] ("," module ["as" identifier])*

"from" relative_module "import" identifier ["as" identifier] ("," identifier ["as" identifier])*

"from" relative_module "import" "(" identifier ["as" identifier] ("," identifier ["as" identifier])* [","] ")"

"from" relative_module "import" "*"
"""


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
            lines.append(t.line.partition("#")[0])
            lineno = t.start[0]
    return " ".join("".join(lines).split()).strip()


def list_imports(tokens) -> Iterator[str]:
    for tl in token_lines(tokens):
        t = tl[0]
        if t.type == token.NAME and t.string in ("from", "import"):
            yield join_lines(tl)


def split_import(line):
    fr, _, im = line.partition('import')
    if fr:
        fr, base = fr.split()
        assert fr == "from"
    else:
        base = ""
    im = im.replace("(", "").replace(")", "")
    parts = [p.split()[0] for p in im.split(",")]

    return base, parts



if __name__ == '__main__':
    for i in sys.argv[1:]:
        print(f"{i}:")
        with open(i) as fp:
            tokens = list(generate_tokens(fp.readline))
            for i in list_imports(tokens):
                print(split_import(i))
