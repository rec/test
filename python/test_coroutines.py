values = []


def coroutine():
    while True:
        value = (yield)
        print(value)


def coroutine2():
    value = 'hello'
    while True:
        value = 2 * (yield value)
        print(value)


def coroutine7():
    value = None
    while True:
        value = 2 * (yield value)
        print('Value')


def process(it):
    for i in it:
        yield i * 10


def connect():
    pass
