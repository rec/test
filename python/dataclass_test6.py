from dataclasses import dataclass
from functools import cached_property


@dataclass
class Data:
    one: str = 'one'

    @property
    def two(self):
        return 'two'

    @cached_property
    def three(self):
        return 'three'

    FOUR = 'four'
