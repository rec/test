import fileinput
import re

START_OF_FILE = re.compile(r'>>>\s+Lint for (.*\.py):\s*')
START_OF_ERROR = re.compile(r'\s*Error \([A-Z_]+\) .*')
ERROR_LINE = re.compile(r'\s*>>>\s*(\d+)  \|  .*')

def pr(*a):
    if False:
        print(*a)


def fix_lint():
    stack = []
    filename = ''

    def print_stack():
        print(*stack, sep='', end='')
        stack.clear()

    for line in fileinput.input():
        if m := START_OF_FILE.match(line):
            pr(' --> START_OF_FILE')
            print_stack()
            filename = m.group(1)
            print(line, end='')
        elif START_OF_ERROR.match(line):
            pr(' --> START_OF_ERROR')
            print_stack()
            stack.append(line)
        elif m := ERROR_LINE.match(line):
            pr(' --> ERROR_LINE')
            lineno = int(m.group(1))
            print(f'{filename}:{lineno}:')
            print()
            stack.append(line)
            print_stack()
        elif stack:
            stack.append(line)
            pr(' --> APPEND')
        else:
            print(line, end='')

    print_stack()


if __name__ == "__main__":
    fix_lint()
