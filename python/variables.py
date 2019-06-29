foo = 23

def func(foo=False):
    print(foo, locals()['foo'], globals()['foo'])

func()
