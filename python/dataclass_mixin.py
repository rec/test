import dataclasses as dc


@dc.dataclass
class One:
    a: int = 1
    b: str = 'B'


@dc.dataclass
class Two:
    c: float = 23.5
    d: str = 'D'


@dc.dataclass
class Three(One, Two):
    pass
