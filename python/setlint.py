import argparse
import tokenize as tok
import typing as t

_HELP_APPLY_PATCHES = 'Actually fix any issues, if possible'
_HELP_EXCLUDE = 'Files or directories to exclude'
_HELP_INCLUDE = 'Files or directories to include'

TOKEN_TYPES = tok.NAME, tok.STRING, tok.OP


def get_tokens(filename):
    with open(filename, 'rb') as fp:
        buffer = []
        for t in tok.tokenize(fp.readline):
            if t.type in TOKEN_TYPES:
                buffer.append(t)
            elif t.type == tok.NEWLINE:
                yield buffer
                buffer = []
        if buffer:
            yield buffer


def parse_args():
    class HelpFormatter(argparse.HelpFormatter):
        def __init__(self, prog, indent_increment=4, max_help_position=16, width=None):
            super().__init__(prog, indent_increment, max_help_position, width)

    parser = argparse.ArgumentParser(formatter_class=HelpFormatter)
    add = parser.add_argument
    add('files', nargs='*', help=_HELP_BRANCHES)
    add('-a', '--apply-patches', action='store_true', help=_HELP_APPLY_PATCHES)
    add('-e', '--exclude', action='append', help=_HELP_EXCLUDE)
    add('-i', '--include', action='append', help=_HELP_INCLUDE)

    return parser.parse_args()
