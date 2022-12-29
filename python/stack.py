import inspect
import traceback

def foo():
    bar(1)


def bar(x):
    baz(x, 12)


def baz(x, y):
    frame = traceback.extract_stack()[-2]
    print(frame.filename)
    print(dir(frame))

    stack = inspect.stack()
    print(stack[0], stack[1])


if __name__ == '__main__':
    foo()
