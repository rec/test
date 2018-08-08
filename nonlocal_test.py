def f():
    x = 2

    def g():
        nonlocal x
        x = 3

    g()

    return x


print(f())
