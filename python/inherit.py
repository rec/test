# class Foo:
#     class Bar(Foo):
#         pass


class Parent1:
    def foo(self):
        return 'parent1'


class Parent2:
    def foo(self):
        return 'parent2'


class Child(Parent1, Parent2):
    pass


print(Child().foo())
