import dataclasses as dc
import functools
import token
from tokenize import tokenize, TokenInfo
from token_line import TokenLine
from omitted_lines import OmittedLines

TOKEN_TYPES = token.NAME, token.STRING, token.OP, token.NEWLINE

"""
Python's tokenizer splits Python code into lexical tokens tagged with one of many
token names. We are only interested in a few of these: references to the built-in `set`
will have to be in a NAME token, and we're only care about enough context to see if it's a
really `set` or, say, a method `set`.

TODO:
* handle `def set()` - now test it!
"""


@dc.dataclass
class TokensUsingSet:
    filename: str

    @functools.cached_property
    def token_lines(self) -> list[TokenLine]:
        omitted = OmittedLines(self.filename)
        token_lines: list[TokenLine] = []

        with open(self.filename, "rb") as fp:
            token_line = TokenLine()

            for t in tokenize(fp.readline):
                if t.type == token.NEWLINE:
                    if not omitted(token_line.lines_covered()):
                        token_lines.append(token_line)
                    token_line = TokenLine()
                elif t.type in TOKEN_TYPES:
                    token_line.tokens.append(t)
            assert not token_line.tokens

        return token_lines

    @functools.cached_property
    def tokens(self) -> list[TokenInfo]:
        tokens: list[TokenInfo] = []
        for tl in self.token_lines:
            tokens.extend(tl.tokens_using_set())

        return tokens
