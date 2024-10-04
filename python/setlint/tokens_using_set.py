import functools
import token
from tokenize import tokenize, TokenInfo
from typing import Generator, List, Set, Tuple
from is_token_using_set import is_token_using_set, TokenLine

TOKEN_TYPES = token.NAME, token.STRING, token.OP, token.NEWLINE
OMIT_COMMENT = '# noqa: setlint'

"""
Python's tokenizer splits Python code into lexical tokens tagged with one of many
token names. We are only interested in a few of these: references to the built-in `set`
will have to be in a NAME token, and we're only care about enough context to see if it's a
really `set` or, say, a method `set`.

TODO:
* handle `def set()` - now test it!
"""


class TokensUsingSet:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    @functools.cached_property
    def tokens_using_set(self) -> Tuple[TokenInfo]:
        tokens: List[TokenInfo] = []
        for tl in self._token_lines():
            tokens.extend(t for i, t in enumerate(tl) if is_token_using_set(tl, i))
        return tuple(tokens)

    def _all_tokens(self) -> Generator[TokenInfo, None, None]:
        with open(self.filename, 'rb') as fp:
            for t in tokenize(fp.readline):
                if t.type in TOKEN_TYPES:
                    yield t

    def _token_lines(self) -> Generator[TokenLine, None, None]:
        buffer: TokenLine = []

        for t in self._all_tokens():
            if t.type == token.NEWLINE:
                if not self._is_omitted(buffer):
                    yield buffer
                buffer = []
            else:
                buffer.append(t)
        assert not buffer

    def _is_omitted(self, tl: TokenLine) -> bool:
        # A TokenLine might span multiple physical lines
        lines = {i for tok in tl for i in (tok.start[0], tok.end[0])}
        return self._omitted_lines.intersection(lines)

    @functools.cached_property
    def _omitted_lines(self) -> Set[int]:
        lines = set()
        with open(self.filename) as fp:
            for i, s in enumerate(fp):
                if s.rstrip().endswith(OMIT_COMMENT):
                    lines.add(i + 1)  # Tokenizer lines start at 1
        return lines


def tokens_using_set(filename: str) -> Generator[TokenInfo, None, None]:
    return TokensUsingSet(filename).tokens_using_set
