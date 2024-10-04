import dataclasses as dc
import functools
import token
from tokenize import tokenize, TokenInfo
from typing import List
from is_token_using_set import is_token_using_set, TokenLine
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
    def token_lines(self) -> List[TokenInfo]:
        omitted = OmittedLines(self.filename)
        token_lines: List[TokenLine] = []

        with open(self.filename, 'rb') as fp:
            buffer: TokenLine = []

            for t in tokenize(fp.readline):
                if t.type == token.NEWLINE:
                    if not omitted(buffer):
                        token_lines.append(buffer)
                    buffer = []
                elif t.type in TOKEN_TYPES:
                    buffer.append(t)
            assert not buffer

        return token_lines

    @functools.cached_property
    def tokens(self) -> List[TokenInfo]:
        tokens: List[TokenInfo] = []
        for tl in self.token_lines:
            tokens.extend(t for i, t in enumerate(tl) if is_token_using_set(tl, i))

        return tokens
