

def a(x=1, y=2):
    def b():
        p = x
        q = y
        return dict(locals())

    return b()

print(a())
