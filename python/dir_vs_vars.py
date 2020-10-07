class Foo:
    bar = 1

    def __init__(self):
        self.baz = 1

    def __call__(self):
        pass


class Bar(Foo):
    bing = 1

    def __init__(self):
        super().__init__()
        self.boing = 2

    def call(self):
        pass


b = Bar()
print(vars(b))
print(b.__dict__)
print(dir(b))
print(set(b.__dict__) == set(dir(b)))
