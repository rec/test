import json


def maker(name):
    def f(x):
        print(name, x)
        return x

    return f
