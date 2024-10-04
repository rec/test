import functools
import token
from tokenize import tokenize, TokenInfo
from typing import Generator, List, Set

TOKEN_TYPES = token.NAME, token.STRING, token.OP, token.NEWLINE
OMIT_COMMENT = '# noqa: setlint'
TokenLine = List[TokenInfo]

"""
Python's tokenizer splits Python code into lexical tokens tagged with one of many
token names. We are only interested in a few of these: references to the built-in `set`
will have to be in a NAME token, and we're only care about enough context to see if it's a
really `set` or, say, a method `set`.

TODO:
* handle `def set()` - now test it!

"""


class FindSetTokens:
    def __init__(self, filename: str) -> None:
        self.name = filename

    def find_set_tokens(self) -> Generator[TokenInfo, None, None]:
        for tl in self._token_lines():
            yield from (t for i, t in enumerate(tl) if self._has_set(tl, i))

    def _has_set(self, tokens: TokenLine, i: int) -> bool:
        # This is where the logic to recognize `set` goes, and
        # probably most bug-fixes.
        t = tokens[i]
        if t.string != 'set' or t.type != token.NAME:
            return False
        if i and tokens[i - 1].string in ('def', '.'):
            return False
        if i >= len(tokens) - 1:
            return True
        u = tokens[i + 1]
        if u.string == '=' and u.type == token.OP:
            return False
        return True

    def _all_tokens(self) -> Generator[TokenInfo, None, None]:
        with open(self.name, 'rb') as fp:
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
        with open(self.name) as fp:
            for i, s in enumerate(fp):
                if s.rstrip().endswith(OMIT_COMMENT):
                    lines.add(i + 1)  # Tokenizer lines start at 1
        return lines


def find_set_tokens(filename: str) -> Generator[TokenInfo, None, None]:
    return FindSetTokens(filename).find_set_tokens()
