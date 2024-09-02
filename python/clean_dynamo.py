import re

M0 = re.compile(r'[A-Z]\d+').match
M1 = re.compile(r'\d\d:\d\d:\d\d\.\d+').match
M2 = re.compile(r'\d+').match

def convert(line):
    s = line.split(maxsplit=3)
    if len(s) > 3 and M0(s[0]) and M1(s[1]) and M2(s[2]):
        return f"{s[0]} {s[3]}"
    else:
        return line


def convert_filename(fn):
    lines = [convert(i) for i in open(fn)]
    open(fn, 'w').writelines(lines)


if __name__ == '__main__':
    import os, sys
    for i in sys.argv[1:]:
        convert_filename(os.path.expanduser(i))
