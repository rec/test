from itertools import takewhile

a = range(10)
it = iter(a)

before = list(takewhile(lambda i: i < 3
