import re

M0 = re.compile(r'[A-Z]\d+').match
M1 = re.compile(r'\d\d:\d\d:\d\d\.\d+').match
M2 = re.compile(r'\d+').match

HEX = re.compile(r'\b(0x[0-9a-f]+)\b')


def _remove_timestamps(line):
    s = line.split(maxsplit=3)
    if len(s) > 3 and M0(s[0]) and M1(s[1]) and M2(s[2]):
        return f"{s[0]} {s[3]}"
    return line


def _canonicalize_hex(line, cache):
    for i, parts in enumerate(HEX.split(line)):
        if i % 2:
            assert HEX.match(h)
            yield cache.setdefault(h, f'0x{len(cache):012x}')
        else:
            yield part


def _convert(line, cache):
    line = _remove_timestamps(line)
    return ''.join(_canonicalize_hex(line, cache))


def convert_filename(fn):
    cache = {}
    lines = list(open(fn))
    open(fn, 'w').writelines(_convert(i, cache) for i in open(fn))


if __name__ == '__main__':
    import os, sys
    for i in sys.argv[1:]:
        convert_filename(os.path.expanduser(i))
