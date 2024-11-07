import fileinput
import re

LINT_LINE = re.compile(r'>>> Lint for ([a-zA-Z0-9/_]*\.py):\s*')
RUFF_LINE = re.compile(r'  Error \([A-Z_]+\) .*')
ERROR_LINE = re.compile(r'    >>>  (\d+)  \|  .*')


def fix_lint():
    stack = []
    filename = ''

    def print_stack():
        print(*stack, sep='', end='')
        stack.clear()

    for line in fileinput.input():
        if m := LINT_LINE.match(line):
            print_stack()
            filename = m.group(1)
            print(line, end='')
        elif RUFF_LINE.match(line):
            print_stack()
            stack.append(line)
        elif m := ERROR_LINE.match(line):
            lineno = int(m.group(1))
            print(f'{filename}:{lineno}:')
            print()
            stack.append(line)
            print_stack()
        elif stack:
            stack.append(line)
        else:
            print(line, end='')

    print_stack()


if __name__ == "__main__":
    fix_lint()
