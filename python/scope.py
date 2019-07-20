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


def test4(param=1):
    def inner(p2=2):
        print('locals', *locals().keys())
        print('globals', *globals().keys())

    inner()

if True:
    test4()
else:
    test()
    test2()
    test3()
