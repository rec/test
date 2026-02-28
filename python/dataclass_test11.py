import dataclasses as dc


@dc.dataclass(frozen=True)
class Child:
    name: str = 'kid'
    age: int = 3


@dc.dataclass(frozen=True)
class Dog:
    name: str = 'woof'


@dc.dataclass(frozen=True)
class Family:
    child: Child = Child()
    dog: Dog = Dog()


print(f := Family())
print(d := dc.asdict(f))
print(f2 := Family(**d))
