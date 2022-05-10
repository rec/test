def test(*args, f=None):
    if not f:
        def f(*a):
            print(*a)

    f(*args)


test(1, 2, 3)
test(2, 5, f=lambda *a: print('xxx', *a))
