def foo(a, b):
    c, d = 1, 2

    def bar(e, f):
        d = 2
        return locals()

    return bar(7, 2)


print(foo(1, 2))
