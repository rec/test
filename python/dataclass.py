from dataclasses import dataclass

@dataclass
class One:
    one: int = 23


@dataclass
class Two(One):
    two: int
    three: int = 32
