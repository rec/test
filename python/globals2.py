def glob():
    global GLOBAL
    print('!!!', GLOBAL)
    GLOBAL = 2


def glob2():
    print(GLOBAL)


glob()
glob2()
