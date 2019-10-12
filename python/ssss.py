# Sort Python includes in all python files or in its arguments
from pathlib import Path
import os
import shutil
import sys

_BEFORE, _SORTING, _BETWEEN, _AFTER = range(4)


def _filter(fp):
    imports, between = [], []
    state = _SORTING

    for line in fp:
        if state is _AFTER:
            yield line

        elif line.startswith('import ') or line.startswith('from '):
            state = _SORTING

            yield from between
            between.clear()
            imports.append(line)

        elif line.startswith('#') or line.startswith(' ') or not line.strip():
            if state is _BEFORE:
                yield line
            else:
                state = _BETWEEN
                between.append(line)
        else:
            state = _AFTER
            imports.sort()
            yield from imports
            yield from between
            yield line


def ssss():
    for fname in sys.argv[1:] or Path().glob('**/*.py'):
        tmp_file = str(fname) + '.tmp'
        try:
            with open(fname) as fin, open(tmp_file, 'w') as fout:
                fout.writelines(_filter(fin))
        except Exception:
            os.remove(tmp_file)
            raise

        shutil.move(tmp_file, fname)
        print('Written', fname)


if __name__ == '__main__':
    ssss()
