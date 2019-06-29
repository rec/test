def test(x):
    foo = None

    if x is True:
        def foo():
            print('yes')
    elif not x:
        def foo():
            print('no')

    return foo

print(test(1))
test(True)()
test(False)()
