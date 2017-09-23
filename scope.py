def test():
    x = 1
    f = lambda: x

    x = 2
    print(f())


test()
