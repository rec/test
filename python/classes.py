@staticmethod
def foo(x):
    return x + 1


class Bar:
    baz = foo
    bing = 1, 2, 3
    bong = bing
    BOOM = 12

    if True:
        bop = 17

    if False:
        bongo = 12

    @staticmethod
    def foo(bar, baz):
        return foo

    def __init__(self, boom=BOOM):
        self.boom = boom
        self.boing = self.BOOM


class Bang:
    Bing = Bar


bar = Bar()
print(bar.baz(1))
print(Bang.Bing)
print(getattr(bar, 'bop', '(none)'))
print(getattr(bar, 'bongo', '(none)'))
