from collections import Counter
from itertools import accumulate
import operator
import math

maxint = 9_223_372_036_854_775_807
FILENAME = '/Users/tom/Downloads/all-words.txt'
FILENAME = '/code/num_name/google-10000-english.txt'

def get(filename=FILENAME):
    lines = (i.strip() for i in open(filename))
    yield from (i for i in lines if i.islower())


def words(filename=FILENAME):
    c = Counter(len(i) for i in get(filename))
    keys, values = zip(*sorted(c.items()))
    values = accumulate(values, operator.add)
    # values = [math.log(maxint) / math.log(i) for i in values]

    for kv in zip(keys, values):
        print(*kv, sep=': ')


def shorter(filename=FILENAME, length=5):
    lines = (i for i in get(filename) if len(i) == length)
    for line in lines:
        print(line)


shorter()
