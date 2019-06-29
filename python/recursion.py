def f(x):
    print('f', x)
    if x > 0:
        g(x - 1)

def g(x):
    print('g', x)
    if x > 0:
        f(x - 1)


g(10)
