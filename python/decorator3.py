from functools import wraps, partial

class Class:
    pass

ac = Class()

def mock_input_decorator(func=None, options=None):
    if func == None:  # Better - if func is None
        return partial(mock_input_decorator, **options)

    @wraps(func)
    def wrapped(*args, **kwargs):
        def wrapper(s="p"):
            return options.pop()
        ac.input = wrapper
        return func(*args, **kwargs)
    return wrapped


# @mock_input_decorator(["1"])  # this wouldn't work.
@mock_input_decorator(choice=["1"])
def test_get_input():
    print('inside!')

@mock_input_decorator
def test_get_input2():
    print('inside 2!')


print(test_get_input())
print(test_get_input2())
