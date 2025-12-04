from functools import cache


def fn(i):
    @cache
    def inner():
        return i

    return inner


print(fn(0)())
print(fn(1)())
