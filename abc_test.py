import abc


class Abstract(abc.ABC):
    @abc.abstractmethod
    def foo(self):
        pass


class Child(Abstract):
    def bar(self):
        pass


class MixIn:
    def foo(self):
        print('found the mixin')


class GrandChild(Child, MixIn):
    pass


GrandChild().foo()
