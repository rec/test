from icecream import ic

# ic.configureOutput(prefix='🍦 ')
hello = 'hello'


def foo():
    ic('foo!')
    ic(hello)
    ic(ic)
    ic()


ic('hello')
ic(hello)
ic(ic)
ic()
foo()
