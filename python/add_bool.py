import os
import re
import sys
import typing as t


WRITE = os.environ.get("ADD_BOOL_WRITE")
# SUB_RE = re.compile(r"\bdef (_?)is_.*\(.*\):")
SUB_RE = re.compile(r"\bdef (_?)has_.*\(.*\):")
VERBOSE = not True


def add_bool():
    if not (argv := sys.argv[1:]):
        lines, changed = _fix_stream(sys.stdin)
        for line in lines:
            sys.stdout.write(line)
        sys.exit(changed)

    all_changed = 0
    changed_files = 0
    for file in argv:
        if VERBOSE:
            print("Reading", file, file=sys.stderr)
        with open(file) as fp:
            lines, changed = _fix_stream(fp)
        if changed:
            print(f"{file}: {changed} changes", file=sys.stderr)
            all_changed += changed
            changed_files += 1
            if WRITE:
                with open(file, 'w') as fp:
                    for line in lines:
                        fp.write(line)
    print(len(argv), "files,", changed_files, "changed,", all_changed, "changed lines", file=sys.stderr)


def _fix_stream(it: t.Iterator[str]) -> tuple[list[str], bool]:
    lines = []
    changed = 0
    for line in it:
        sub = SUB_RE.sub((lambda m: f"{m.group()[:-1]} -> bool:"), line)
        lines.append(sub)
        if line != sub:
            changed += 1

    return lines, changed


if __name__ == '__main__':
    add_bool()
