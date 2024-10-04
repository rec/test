import token
from typing import Sequence
from tokenize import TokenInfo

TokenLine = Sequence[TokenInfo]


def is_token_using_set(tokens: TokenLine, i: int) -> bool:
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
