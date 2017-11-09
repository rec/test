def test():
    x = 1
    f = lambda: x

    x = 2
    print(f())


def test2(omit=None):
    def scrub(attrs):
        return tuple(a for a in attrs if a not in omit)

    omit = omit or ()

    print(scrub('abc'))


test()
test2()
