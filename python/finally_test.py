
class Foo:
    bar = False

    def method(self):
        try:
            return 0
        finally:
            self.bar = True

foo = Foo()
print(foo.bar)
print(foo.method())
print(foo.bar)
