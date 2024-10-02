import argparse
import typing as t

_HELP_APPLY_PATCHES = 'Actually fix any issues, if possible'
_HELP_EXCLUDE = 'Files or directories to exclude'
_HELP_INCLUDE = 'Files or directories to include'

STATES = COMMENT, SINGLE_QUOTE, DOUBLE_QUOTE = '#', "'''", '"""'


def split_line(state, line, offset=0) -> t.Iterator[t.Tuple[str, str, lint]]:
    if state != COMMENT:
        before, sep, after = line.partition(state)
        if after:
            yield from split_line(COMMENT, after, offset + len(before + sep))
        return

    splits = [line.partition(s) for s in STATES]
    splits = [(b, s, a) for b, s, a in splits if s]
    if splits:
        splits.sort(key=lambda x: len(x[0]))
        before, state, after = splits[0]
        if state == COMMENT and not after.strip.startswith('noqa: setlint'):
            yield state, before, offset
    else:
        yield state, line, offset


def split_lines(lines):
    state = COMMENT
    for number, line in enumerate(lines):
        for state, part, offset in split_line(state, line, offset):
            pass


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
