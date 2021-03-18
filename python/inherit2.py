class Parent1:
    def __call__(self):
        return 'parent1'


class Parent2:
    def foo(self):
        return 'parent2'


class Child1(Parent1):
    pass
