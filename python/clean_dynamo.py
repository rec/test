import os
import re

M0 = re.compile(r'[A-Z]\d+').match
M1 = re.compile(r'\d\d:\d\d:\d\d\.\d+').match
M2 = re.compile(r'\d+').match


def convert_filename(fn):
    for line in open(fn):
        s = line.split(maxsplit=3)
        if len(s) > 3 and M0(s[0]) and M1(s[1]) and M2(s[2]):
            print(s[0], s[3])
        else:
            pass
            # print(line)


if __name__ == '__main__':
    import sys

    convert_filename(os.path.expanduser(sys.argv[1]))
