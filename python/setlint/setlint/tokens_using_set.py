import dataclasses as dc
import token
from tokenize import tokenize, TokenInfo
from .token_line import TokenLine
from .omitted_lines import OmittedLines
from typing import Iterator

TOKEN_TYPES = token.NAME, token.STRING, token.OP, token.NEWLINE

"""
Python's tokenizer splits Python code into lexical tokens tagged with one of many
token names. We are only interested in a few of these: references to the built-in `set`
will have to be in a NAME token, and we're only care about enough context to see if it's a
really `set` or, say, a method `set`.

TODO:
* handle `def set()` - now test it!
"""


def all_token_lines(filename: str) -> Iterator[TokenLine]:
    token_line = TokenLine()

    with open(filename, "rb") as fp:
        for t in tokenize(fp.readline):
            token_line.tokens.append(t)
            if t.type == token.NEWLINE:
                yield token_line
                token_line = TokenLine()

    if token_line.tokens:
        yield token_line


def token_lines(filename: str) -> Iterator[TokenLine]:
    omitted = OmittedLines(filename)
    for line in all_token_lines(filename):
        if not omitted(line.lines_covered()):
            yield line


def tokens(filename: str) -> Iterator[TokenInfo]:
    for tl in token_lines(filename):
        yield from tl.tokens_using_set()
