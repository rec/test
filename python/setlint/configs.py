import argparse
import json
from typing import Sequence

_HELP_EXCLUDE = 'Files or directories to exclude'
_HELP_FIX = 'Actually fix any issues, if possible'
_HELP_INCLUDE = 'Files or directories to include'
_HELP_FILES = 'Files to check. Overrides --exclude and --include if set'


def add_configs(args: argparse.Namespace, filename: str) -> argparse.Namespace:
    try:
        with open(filename) as fp:
            config = json.load(fp)
    except FileNotFoundError:
        config = {}

    if bad := set(config) - set(vars(args)):
        s = '' if len(bad) == 1 else 's'
        bad = ', '.join(sorted(bad))
        raise ValueError(f'Unknown arg{s}: {bad}')

    for k, v in config.items():
        if k == 'fix' and args.fix is None:
            args.fix = v
        else:
            setattr(args, k, getattr(args, k) or v)


def get_files(args: argparse.Namespace) -> Sequence[str]:
    if args.files:
        return args.files
    raise NotImplementedError


def make_parser() -> argparse.ArgumentParser:
    class HelpFormatter(argparse.HelpFormatter):
        def __init__(self, prog, indent_increment=4, max_help_position=16, width=None):
            super().__init__(prog, indent_increment, max_help_position, width)

    parser = argparse.ArgumentParser(formatter_class=HelpFormatter)
    add = parser.add_argument
    add('files', nargs='*', help=_HELP_FILES)
    add('-e', '--exclude', action='append', help=_HELP_EXCLUDE)
    add('-f', '--fix', default=None, action='store_true', help=_HELP_FIX)
    add('-i', '--include', action='append', help=_HELP_INCLUDE)
    return parser


def get_args(config_filename: str) -> argparse.Namespace:
    args = make_parser().parse_args()
    add_configs(args, config_filename)
    return args
