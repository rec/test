import dataclasses as dc
import token
from typing import Generator, List
from tokenize import TokenInfo


@dc.dataclass
class TokenLine:
    """A logical line of tokens separated by token.NEWLINE.
    There might be physical newlines in it, separated by token.NL.
    """

    tokens: List[TokenInfo] = dc.field(default_factory=list)

    def is_token_using_set(self, i: int) -> bool:
        # This method has to be on the full line, because we look behind and ahead.
        # This is where the logic to recognize `set` goes, and # probably most bug-fixes.
        t = self.tokens[i]
        if t.string != "set" or t.type != token.NAME:
            return False
        elif i and self.tokens[i - 1].string in ("def", "."):
            return False
        elif i >= len(self.tokens) - 1:
            return True
        else:
            u = self.tokens[i + 1]
            return not (u.string == "=" and u.type == token.OP)

    def tokens_using_set(self) -> Generator[TokenInfo, None, None]:
        for i, t in enumerate(self.tokens):
            if self.is_token_using_set(i):
                yield t

    def lines_covered(self) -> List[int]:
        lines = sorted(i for t in self.tokens for i in (t.start[0], t.end[0]))
        return list(range(lines[0], lines[-1] + 1)) if lines else []
