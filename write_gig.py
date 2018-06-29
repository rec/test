LINE = 'abcdefghijklnmopqrtsuvwx\n'
ONE_GIG = 1000 * 1000 * 1000
LINES = ONE_GIG // len(LINE)

with open('/tmp/big.txt', 'w') as fp:
    for i in range(LINES):
        fp.write(LINE)
