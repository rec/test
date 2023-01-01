from dataclasses import dataclass
import functools
import itertools

COUNT = itertools.count(1)


class Class:
    @functools.cache
    def count(self):
        return next(COUNT)


@dataclass(frozen=True)
class Dataclass:
    @functools.cache
    def count(self):
        return next(COUNT)


def test_cache(cls):
    a, b = cls(), cls()
    print(f'{a.count()=} {b.count()=}')
    assert a.count() + 1 == b.count()


test_cache(Class)
test_cache(Dataclass)
