class Outer:
    class Inner:
        A = 1
        B = 1

    class Inner2(Inner):
        B = 2


o = Outer.Inner2()
print(o.A, o.B)
