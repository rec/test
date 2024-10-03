import dataclasses as dc
import functools
import token
from tokenize import tokenize, TokenInfo
from typing import Iterator, List, Sequence, Set

TOKEN_TYPES = token.NAME, token.STRING, token.OP, token.NEWLINE
OMIT_COMMENT = '# noqa: setlint'


@dc.dataclass
class FileRecord:
    name: str

    def all_tokens(self) -> Sequence[TokenInfo]:
        with open(self.name, 'rb') as fp:
            yield from tokenize(fp.readline)

    def token_lines(self) -> Iterator[Sequence[Sequence[TokenInfo]]]:
        buffer: List[TokenInfo] = []

        for t in self.all_tokens():
            if self.is_accepted(t):
                if t.type == token.NEWLINE:
                    yield buffer
                    buffer = []
                else:
                    buffer.append(t)
        assert not buffer

    def tokens_with_sets(self):
        for tl in self.token_lines():
            for i, t in enumerate(tl):
                if (
                    t.type == token.NAME
                    and t.string == 'set'
                    and (not i or tl[i - 1].string != '.')
                ):
                    yield TokenInFile(self, t)

    @functools.cached_property
    def omitted_lines(self) -> Set[int]:
        lines = {}
        with open(self.name) as fp:
            for i, s in enumerate(fp):
                if s.rstrip().endswith(OMIT_COMMENT):
                    lines.add(i + 1)  # Tokenizer lines start at 1
        return lines

    def is_accepted(self, t: TokenInfo) -> bool:
        return (
            t.type in TOKEN_TYPES and
            not self.omitted_lines.intersection([t.start[0], t.end[0]])
        )


@dc.dataclass
class TokenInFile:
    file_record: FileRecord
    token: TokenInfo
