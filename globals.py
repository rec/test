GLOBAL = 1

def glob():
    global GLOBAL

    def f():
        GLOBAL = 3

    GLOBAL = 2
    f()

glob()


def glob2():
    global GLOBAL2
    GLOBAL2 = 3


print(GLOBAL)
print(GLOBAL2)
