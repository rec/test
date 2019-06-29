import sys

lines = 0

try:
    with sys.stdout as output:
        with sys.stdin as input:
            for i in input:
                output.write(i)
                lines += 1
finally:
    print('!!!!', lines, file=sys.stderr)
