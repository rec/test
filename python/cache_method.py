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
class CachedProperty:
    def count(self):
        return self._count

    @functools.cached_property
    def _count(self):
        return next(COUNT)


def test_ok(cls):
    a, b = cls(), cls()
    print(f'ok:   {a.count()=} {b.count()=}')
    assert a.count() + 1 == b.count()


test_ok(Class)
test_ok(LruClass)
test_ok(CachedProperty)


@dataclass(frozen=True, eq=False)
class Cache:
    @functools.cache
    def count(self):
        return next(COUNT)


@dataclass(frozen=True, eq=False)
class Lru:
    @functools.lru_cache(maxsize=None)
    def count(self):
        return next(COUNT)


def test_fails(cls):
    a, b = cls(), cls()
    print(f'FAIL: {a.count()=} {b.count()=}')
    assert a.count() == b.count()


test_fails(Cache)
test_fails(Lru)
