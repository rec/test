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

    FOUR = 'four'

d = Data()
print(d)
print(d.two)
print(d.three)
