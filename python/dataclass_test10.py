import dataclasses as dc


class Parent:
    def __post_init__(self):
        print('   PARENT')


@dc.dataclass
class Child1(Parent):
    name: str = 'kid'


@dc.dataclass
class Child2(Parent):
    def __post_init__(self):
        super().__post_init__()
    name: str = 'kid'


print('child1', Child1())
print('child2', Child2())
