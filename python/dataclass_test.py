from dataclasses import dataclass
from pathlib import Path


@dataclass
class Parent:
    path: str = 'one'


@dataclass
class Child(Parent):
    path: str = 'two'
