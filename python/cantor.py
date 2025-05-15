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
