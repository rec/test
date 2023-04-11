from dataclasses import dataclass


@dataclass(frozen=True)
class C:
    i: int = 0
    s: str = ''

    @property
    def foo(self):
        return self.__dict__.get('foo')

    @foo.setter
    def foo(self, x):
        self.__dict__['foo'] = x


c = C()
c.foo = 10
print(c.foo)
