import argparse
import json
from typing import Sequence


def add_configs(args: argparse.Namespace, filename: str) -> argparse.Namespace:
    try:
        with open(filename) as fp:
            config = json.load(fp)
    except FileNotFoundError:
        config = {}

    if bad := set(config) - set(vars(args)):
        s = "" if len(bad) == 1 else "s"
        bad_name = ", ".join(sorted(bad))
        raise ValueError(f"Unknown arg{s}: {bad_name}")

    for k, v in config.items():
        if k == "fix" and args.fix is None:
            args.fix = v
        else:
            setattr(args, k, getattr(args, k) or v)

    return args


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

    add("files", nargs="*", help="Files or directories to exclude")
    add("-e", "--exclude", action="append", help="Files to check.")
    add("-f", "--fix", default=None, action="store_true", help="Fix any issues")
    return parser


def get_args(config_filename: str) -> argparse.Namespace:
    args = make_parser().parse_args()
    add_configs(args, config_filename)
    return args
