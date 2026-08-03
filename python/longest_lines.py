import sys

for s in sorted((i.rstrip() for f in sys.argv for i in open(f)), key=len, reverse=True):
    print(f'{len(s):3}: {s}')
