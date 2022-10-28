from dataclasses import dataclass
from functools import cached_property
from typing import Callable


@dataclass(name='wombat')
class _Empty:
    __name__ = 'Wombat'
    value = None

print(_Empty())
