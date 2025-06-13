import re
import sys
import typing as t

WRITE = False


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
            all_changed += 1
            if WRITE:
                with open(file, 'w') as fp:
                    for line in lines:
                        fp.write(line)
            print("Changed", file, file=sys.stderr)
    print(len(argv), "files", all_changed, "changes", file=sys.stderr)


SUB_RE = re.compile(r"\bdef (_?)is_.*\(.*\):")
SUB_RE = re.compile(r"\bdef (_?)is_.*\(.*\):")

def _fix_stream(it: t.Iterator[str]) -> tuple[list[str], bool]:
    lines = []
    changed = False
    for line in it:
        sub = SUB_RE.sub((lambda m: f"{m.group()[:-1]} -> bool:"), line)
        lines.append(sub)
        changed = changed or line != sub
        assert not changed, (line, sub)

    return lines, changed

if __name__ == '__main__':
    add_bool()
