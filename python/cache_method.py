from dataclasses import dataclass
import functools
import itertools

COUNT = itertools.count(1)


class Class:
    @functools.cache
    def count(self):
        return next(COUNT)


class LruClass:
    @functools.lru_cache(maxsize=None)
    def count(self):
        return next(COUNT)


@dataclass(frozen=True)
class Dataclass:
    @functools.cache
    def count(self):
        return next(COUNT)


@dataclass(frozen=True)
class LruDataclass:
    @functools.lru_cache(maxsize=None)
    def count(self):
        return next(COUNT)


class Child(Class):
    pass


@dataclass(frozen=True)
class DataChild(Class):
    pass


def test_ok(cls):
    a, b = cls(), cls()
    print(f'{a.count()=} {b.count()=}')
    assert a.count() + 1 == b.count()


def test_fails(cls):
    a, b = cls(), cls()
    print(f'{a.count()=} {b.count()=}')
    assert a.count() == b.count()


test_ok(Class)
test_fails(Dataclass)

test_ok(Child)
test_fails(DataChild)

test_ok(LruClass)
test_fails(LruDataclass)
