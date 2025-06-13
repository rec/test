import os
import re
import sys
import typing as t


WRITE = os.environ.get("ADD_BOOL_WRITE")


def add_bool():
    if not (argv := sys.argv[1:]):
        lines, changed = _fix_stream(sys.stdin)
        for line in lines:
            sys.stdout.write(line)
        sys.exit(changed)

    all_changed = 0
    for file in argv:
        with open(file) as fp:
            lines, changed = _fix_stream(fp)
        if changed:
            print("Found", file, file=sys.stderr)
            all_changed += 1
            if WRITE:
                with open(file, 'w') as fp:
                    for line in lines:
                        fp.write(line)
    print(len(argv), "files", all_changed, "changes", file=sys.stderr)


SUB_RE = re.compile(r"\bdef (_?)is_.*\(.*\):")


def _fix_stream(it: t.Iterator[str]) -> tuple[list[str], bool]:
    lines = []
    changed = False
    for line in it:
        sub = SUB_RE.sub((lambda m: f"{m.group()[:-1]} -> bool:"), line)
        lines.append(sub)
        changed = changed or line != sub

    return lines, changed

if __name__ == '__main__':
    add_bool()
