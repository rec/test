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


def test3():
    for i in range(3):
        j = i
    print(i, j)


test()
test2()
test3()
