import sys
from .files import resolve_python_files
from .python_file import PythonFile
from . import configs, fix_set_tokens

CONFIG_FILE = "setlint.json"


def main():
    args = configs.get_args(CONFIG_FILE)
    if not (python_files := resolve_python_files(args.files, args.exclude)):
        sys.exit("No files selected")

    def pr(*a, **ka) -> None:
        if args.verbose:
            print(*a, file=sys.stderr, **ka)

    for f in python_files:
        args.verbose and print(f, "Reading", file=sys.stderr)
        pf = PythonFile(f)
        if not pf.set_tokens:
            pr(f, "OK")
            continue
        if not args.fix or args.verbose:
            for t in pf.set_tokens():
                pass
        if args.fix:
            lines, count = fix_set_tokens(pf)
            with open(f, "w") as fp:
                fp.writelines(lines)
            print(f, f"fixed {count} error{'s' * (count != 1)}", file=sys.stderr)


if __name__ == "__main__":
    main()
