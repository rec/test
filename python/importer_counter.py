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
            lines.append(t.line)
            lineno = t.start[0]
    return " ".join("".join(lines).split()).strip()


def list_imports(tokens) -> Iterator[str]:
    for tl in token_lines(tokens):
        t = tl[0]
        if t.type == token.NAME and t.string in ("from", "import"):
            yield join_lines(tl)


def imports(token_lines) -> Iterator[str]:
    for tl in token_lines:
        if (t := tl[0]).type != token.NAME:
            pass
        elif t.string == "from":
            yield from _from(tl[1:])
        elif t.string == "import":
            yield from _import(tl[1:])


def _from(tokens: list[TokenInfo]):
    stack = []
    for i, t in enumerate(tokens):
        if t.type == token.NAME:
            if t.string == "import":
                break
            else:
                stack.append(t.string)

        elif t.type == token.OP:
            assert t.string == "."
            stack.append(t.string)

    base = "".join(reversed(stack))
    yield from (f"{base}.{i}" for i in _import(tokens[i + 1::]))


def _import(tokens: list[TokenInfo]):
    stack = []
    for t in tokens:
        if t.type == token.NAME:
            stack.append(t.string)
        elif t.type != token.OP:
            continue
        elif t.string == ".":
            stack.append(t.string)
        elif t.string == ",":
            assert stack
            yield "".join(reversed(stack))
            stack = []
        else:
            assert False

    if stack:
        yield "".join(reversed(stack))


if __name__ == '__main__':
    for i in sys.argv[1:]:
        print(f"{i}:")
        with open(i) as fp:
            tokens = list(generate_tokens(fp.readline))
            if False:
                tl = token_lines(tokens)
                print('Token count', len(tokens), 'tl', len(tl))
                for line in imports(tl):
                    print(line)
            else:
                for i in list_imports(tokens):
                    print(i)
