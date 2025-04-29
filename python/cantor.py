import math

# https://math.stackexchange.com/questions/1377929/

def cantor(*a: int) -> int:
    N = len(a)

    def c(i: int) -> int:
        return math.comb(i - 1 + sum(a[N - j - 1] for j in range(i)), i)

    return sum(c(i) for i in range(1, N + 1))


for i in range(4):
    print(i, cantor(i))

print()

for i in range(4):
    for j in range(4):
        print(i, j, cantor(i, j))

if False:
    for i in range(4):
        for j in range(4):
            for k in range(4):
                  print(i, j, k, cantor(i, j, k))

from typing import Sequence, Iterator


def cantor_count(N: int) -> Iterator[list[int]]:
    def count(*used: int) -> Iterator[list[int]]:
        unused = (i for i in range(N) if i not in used)
        if N == U + 1:
            yield [next(it)]
        else:
            for u in unused:
                for c in count(*used, u):
                    yield [u] + c
