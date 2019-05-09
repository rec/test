FOO = 1

def keys(x):
    return [k for k in x.keys() if not k.startswith('_')]

def foo(bar):
    baz = 3
    print('foo', keys(globals()), keys(locals()), sep='\n')


print('TOP', keys(globals()), keys(locals()), sep='\n')
foo(12)
