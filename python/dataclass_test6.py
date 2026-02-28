import time

from dataclasses import dataclass
from functools import cached_property


@dataclass(frozen=True)
class Data:
    one: str = 'one'

    @property
    def two(self):
        return 'two'

    @cached_property
    def three(self):
        return 'three'

    @cached_property
    def time(self):
        return time.time()

    FOUR = 'four'

d = Data()
print(d)
print(d.two)
print(d.three)

import pickle
print(d.time)
e = pickle.loads(pickle.dumps(d))
print(e.__dict__)

assert e.time != d.time
