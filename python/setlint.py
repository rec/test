import argparse
import token
from tokenize import tokenize, TokenInfo
from typing import Iterator, Sequence, Tuple

_HELP_APPLY_PATCHES = 'Actually fix any issues, if possible'
_HELP_EXCLUDE = 'Files or directories to exclude'
_HELP_INCLUDE = 'Files or directories to include'

TOKEN_TYPES = token.NAME, token.STRING, token.OP

Tokens = Sequence[TokenInfo]


def get_tokens(filename: str) -> Iterator[Tokens]:
    with open(filename, 'rb') as fp:
        buffer = []
        for t in tokenize(fp.readline):
            if t.type in TOKEN_TYPES:
                buffer.append(t)
            elif t.type == token.NEWLINE:
                yield buffer
                buffer = []
        if buffer:
            yield buffer


def get_sets(tl: Tokens) -> Iterator[TokenInfo]:
    def is_set(i, t):
        return (
            t.type == token.NAME
            and t.string in ('set', 'set(')
            and (not i or tl[i - 1].string != '.')
        )

    yield from (t for i, t in enumerate(tl) if is_set(i, t))


def all_sets(filenames: Sequence[str]) -> Iterator[Tuple[str, TokenInfo]]:
    for f in filenames:
        for tl in get_tokens(f):
            for s in get_sets(tl):
                yield f, s


def parse_args() -> argparse.Namespace:
    class HelpFormatter(argparse.HelpFormatter):
        def __init__(self, prog, indent_increment=4, max_help_position=16, width=None):
            super().__init__(prog, indent_increment, max_help_position, width)

    parser = argparse.ArgumentParser(formatter_class=HelpFormatter)
    add = parser.add_argument
    add('files', nargs='*', help=_HELP_BRANCHES)
    add('-a', '--apply-patches', default=None, action='store_true', help=_HELP_APPLY_PATCHES)
    add('-e', '--exclude', action='append', help=_HELP_EXCLUDE)
    add('-i', '--include', action='append', help=_HELP_INCLUDE)

    return parser.parse_args()