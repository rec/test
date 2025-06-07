from typing import Iterator


def tokenize(expr: str) -> Iterator[str]:
    start = -1
    for i, s in enumerate(expr):
        if s.isnumeric():
            if start == -1:
                start = i
        else:
            if start != -1:
                yield expr[start:i]
                start = -1
            if s != " ":
                yield s
    if start != -1:
        yield expr[start:]


for i in ("3 + (1 + 2 * 3)", "2 * 3 + (1 + 2 * (2 + 3))"):
    print(i, list(tokenize(i)))
