from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Parent:
    path: str = 'one'


@dataclass
class Child(Parent):
    path: str = 'two'


@dataclass
class Vehicle0:
    wheels: int = 2

    def __post_init__(self):
        print('one', self._wheels, self.wheels)
        self.wheels = self._wheels

    def set_wheels(self) -> int:
        return self._wheels

    def get_wheels(self, wheels: int):
        self._wheels = wheels


Vehicle.wheels = property(Vehicle.get_wheels, Vehicle.set_wheels)

from dataclasses import dataclass, field


@dataclass
class Vehicle:

    wheels: int = 1

    def get_wheels(self) -> int:
        return self._wheels

    def set_wheels(self, wheels: int):
        self._wheels = wheels


Vehicle.wheels = property(Vehicle.get_wheels, Vehicle.set_wheels)

v = Vehicle()
print(v)

v = Vehicle(wheels=6)
print(v)


@dataclass
class Test:
    _name: str="schbell"

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, v: str) -> None:
        self._name = v
