import re


class Fixer:
    pattern: re.Pattern

    def _replace(self, part):
        raise NotImplementedError

    def _process(self, line):
        for i, part in enumerate(self.pattern.split(line)):
            yield self._replace(part) if i % 2 else part

    def __call__(self, line):
        return ''.join(self._process(line))


class Hex(Fixer):
    pattern = re.compile(r'\b(0x[0-9a-f]+)\b')

    def __init__(self):
        self._cache = {}

    def _replace(self, part):
        name = f'0x{0xFACE_0000 + len(self._cache):012x}'
        return self._cache.setdefault(part, name)


class TimestampAndPID(Fixer):
    pattern = re.compile(r'([^\s]+ \d\d:\d\d:\d\d\.\d+ \d+ )')

    def _replace(self, part):
        return part.split()[0] + ' '


class CondaUrl(Fixer):
    pattern = re.compile(r'(/home/[^/]+/.conda/envs/[^/]+)')

    def _replace(self, part):
        return '*conda'


class GitUrl(Fixer):
    pattern = re.compile(r'(/home/[^/]+/git[^/]*/pytorch/)')

    def _replace(self, part):
        return '*git/pytorch/'


CONVERTERS = (
    Hex(),
    TimestampAndPID(),
    CondaUrl(),
    GitUrl(),
)


def convert(line):
    for c in CONVERTERS:
        line = c(line)
    return line


def convert_filename(fn):
    lines = list(open(fn))
    converted = [convert(line) for line in lines]
    # os.rename(fn, fn + '.bak')
    with open(fn + '.out', 'w') as fp:
        fp.writelines(converted)


if __name__ == '__main__':
    import os, sys
    for i in sys.argv[1:]:
        convert_filename(os.path.expanduser(i))
