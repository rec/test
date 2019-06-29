def f():
    def g():
        return 1

    g = lambda: 3

    return g

print(f()())
