

from attr import Factory, attrib, attrs, dataclass

@attrs
class Parent(object):
    x = attrib(default=1)
    y = attrib(default=2)

@attrs
class Child(Parent):
    x = attrib(default = 3)
    xx = attrib(default=19)
    zz = attrib(default=5)

@dataclass
class Parent2(object):
    x: int = 1
    y: int = 2

@attrs
class Child2(Parent2):
    x = attrib(default = 3)
    xx = attrib(default=19)
    zz = attrib(default=5)

@dataclass
class Child3(Parent2):
    x: int = 3
    z: object = Factory(dict)
