import dataclasses as dc


@dc.dataclass
class One:
    one: str = 'one'
    two: int = 2

    asdict = dc.asdict


one = One()
one.three = 'HELLO!'
print(one.asdict())
