import sys
from .files import resolve_python_files
from .lint_file import lint_file
from . import configs

CONFIG_FILE = "setlint.json"


def main():
    args = configs.get_args(CONFIG_FILE)
    if not (python_files := resolve_python_files(args.files, args.exclude)):
        sys.exit("No files selected")

    for f in python_files:
        if not True:
            print(f)
        else:
            lint_file(f, args)


if __name__ == "__main__":
    main()
