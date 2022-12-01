class Callable:
    @classmethod
    def __call__(cls, x):
        print('a', x)


Callable(3)
