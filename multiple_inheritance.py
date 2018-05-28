
class Foo:
    def one(self):
        return 'Foo.self'


class Bar:
    def one(self):
        return 'Bar.self'


class Baz(Foo, Bar):
    def two(self):
        print(Foo.one(self), Bar.one(self), self.one())
        print(super(


Baz().two()
