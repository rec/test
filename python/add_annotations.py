from __future__ import annotations
from pathlib import Path
from typing import Sequence

FROM_FUTURE = 'from __future__ import annotations'
FROM_FUTURE_LINE = FROM_FUTURE + '\n'
ENABLED = False

def annotation_line(p: Path) -> tuple[int | None, list[str]]:
    result = None
    found_class_or_def = False
    with p.open() as fp:
        lines = list(fp)

    for i, line in enumerate(lines):
        if line.startswith(FROM_FUTURE):
            break
        if not line.startswith('#'):
            if result is None:
                result = i
            if line.strip().startswith(("class ", "def ")):
                found_class_or_def = True
                break
    if not found_class_or_def:
        result = None
    return result, lines


def add_imports(paths: Sequence[Path]):
    for p in paths:
        result, lines = annotation_line(p)
        if result is None:
            print('Skipped', p)
        else:
            lines.insert(result, FROM_FUTURE_LINE)
            with p.open('w') as fp:
                fp.writelines(lines)
            print('Rewrote', p)


if __name__ == '__main__':
    import sys

    add_imports([Path(i) for i in sys.argv[1:]])
