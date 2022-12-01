from dataclasses import dataclass, field


@dataclass
class Child:
    d: dict = field(default_factory=dict)
    i: int = 0

    def __setattr__(self, k, v):
        print('child', k, v)
        super().__setattr__(k, v)


@dataclass
class Parent:
    child: Child = field(default_factory=Child)

    def __setattr__(self, k, v):
        print('parent', k, v)
        super().__setattr__(k, v)

Parent()
