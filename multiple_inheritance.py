class Foo:
    def __init__(self):
        print('Foo.__init__')

    def one(self):
        return 'Foo.self'


class Bar:
    def __init__(self):
        print('Bar.__init__')

    def one(self):
        return 'Bar.self'


class Baz(Foo, Bar):
    def two(self):
        print(Foo.one(self), Bar.one(self), self.one())


Baz().two()

# Result:
#   Foo.__init__
#   Foo.self Bar.self Foo.self
