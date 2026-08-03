from functools import cached_property


class Class:
    @cached_property
    def one(self):
        print('here')
        return 23


c = Class()
print('one', c.one)
print('two', c.one)
del c.one
print('three', c.one)
