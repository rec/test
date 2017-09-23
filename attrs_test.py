from attr import attrib, attrs

@attrs
class Parent(object):
    x = attrib(default=1)
    y = attrib(default=2)

@attrs
class Child(Parent):
    xx = attrib(default=19)
    zz = attrib(default=5)
