@staticmethod
def foo(x):
    return x + 1


class Bar:
    baz = foo
    bing = 1, 2, 3
    bong = bing

    @staticmethod
    def foo(bar, baz):
        return foo

class Bang:
    Bing = Bar


bar = Bar()
print(bar.baz(1))
print(Bang.Bing)
