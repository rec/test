class MyDescriptor():
    def __init__(self, initial_value=None, name='my_var'):
        self.var_name = name
        self.value = initial_value

    def __get__(self, obj, objtype):
        print('Getting', self.var_name)
        return self.value

    def __set__(self, obj, value):
        msg = 'Setting {name} to {value}'
        print(msg.format(name=self.var_name, value=value))
        self.value = value


class Foo:
    bar = MyDescriptor(12)
    baz = 2


FOO = Foo()
print(type(Foo.bar), type(FOO.bar), type(Foo.__dict__['bar']))
