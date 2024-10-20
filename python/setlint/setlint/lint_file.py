from .python_file import PythonFile
from .fix_set_tokens import fix_set_tokens
from argparse import Namespace

WINDOW = 5
BEFORE = 2
AFTER = WINDOW - BEFORE - 1
ERROR = "Builtin `set` is deprecated"


def lint_file(filename: str, args: Namespace) -> None:
    def pr(*a, **ka) -> None:
        if args.verbose:
            print(*a, **ka)

    def print_source(i, text):
        if text is None:
            i = ""
            text = ""
        print(f"{i:5} | {text.rstrip()}")

    pr(filename, "Reading")
    pf = PythonFile(filename)
    if not pf.set_tokens:
        pr(filename, "OK")
        return

    if args.fix:
        fix_set_tokens(pf)
        with open(filename, "w") as fp:
            fp.writelines(pf.lines)

        count = len(pf.set_tokens)
        print(f"{filename}: Fixed {count} error{'s' * (count != 1)}")
        if not args.verbose:
            return

    padded = [None] * BEFORE + pf.lines + [None] * AFTER
    padded_line = list(enumerate(padded))
    for i, t in enumerate(pf.set_tokens):
        print()
        (line, start), (line2, end) = t.start, t.end
        assert line == line2
        assert start + 3 == end
        window = padded_line[line - 1 : line - 1 + WINDOW]
        before, after = window[: BEFORE + 1], window[BEFORE + 1 :]

        print(f"{filename}:{line}:{start}: {ERROR}")

        for i, text in before:
            print_source(i + line - BEFORE, text)

        print_source("", " " * start + "^^^\n")

        for line, text in after:
            print_source(i + line - BEFORE, text)
