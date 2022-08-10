from dataclasses import dataclass
from functools import cached_property
from typing import Callable


@dataclass
class Parent:
    one: Callable = str


class Child(Parent):
    def one(self, x):
        return int(x)

print(type(Child().one('12')))
