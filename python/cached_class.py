from functools import cached_property
import time


class Test:
    @cached_property
    @classmethod
    def time(cls):
        return time.time()
