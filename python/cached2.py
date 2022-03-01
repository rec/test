from functools import cached_property


class Class:
    @cached_property
    def foo(self):
        return 23
