import fileinput
import re

LINT_LINE = re.compile(r'>>> Lint for ([a-zA-Z0-9/_]*\.py):\s*')
ERROR_LINE = re.compile(r'    >>>  (\d+)  \|  .*')


def fix_lint():
    stack = []
    filename = ''

    for line in fileinput.input():
        if stack and (m := ERROR_LINE.match(line)):
            lineno = int(m.group(1))
            print(f'{filename}:{lineno}:')
            print(*stack, sep='', end='')
            stack.clear()
        elif stack:
            stack.append(line)
        elif m := LINT_LINE.match(line):
            filename = m.group(1)
            stack.append(line)
        else:
            print(line, end='')

    assert not stack


if __name__ == "__main__":
    fix_lint()
