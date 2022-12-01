from functools import cached_property


class Class:
    @classmethod
    @cached_property
    def foo(cls):
        return 23


print(Class().foo)
