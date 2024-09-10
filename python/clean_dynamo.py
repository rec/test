import re

M0 = re.compile(r'[A-Z]\d+').match
M1 = re.compile(r'\d\d:\d\d:\d\d\.\d+').match
M2 = re.compile(r'\d+').match

HEX = re.compile(r'\b(0x[0-9a-f]+)\b')


def convert(line, cache):
    s = line.split(maxsplit=3)
    if len(s) > 3 and M0(s[0]) and M1(s[1]) and M2(s[2]):
        line = f"{s[0]} {s[3]}"

    parts = HEX.split(line)
    for i in range(1, len(parts), 2):
        h = parts[i]
        assert HEX.match(h)
        try:
            parts[i] = cache[h]
        except KeyError:
            hname = f'0x{len(cache):012x}'
            parts[i] = hname
            cache[h] = hname

    return ''.join(parts)


def convert_filename(fn):
    cache = {}
    lines = [convert(i, cache) for i in open(fn)]
    open(fn, 'w').writelines(lines)


if __name__ == '__main__':
    import os, sys
    for i in sys.argv[1:]:
        convert_filename(os.path.expanduser(i))
