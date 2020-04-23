def new_class(parent):
    class Class(parent):
        def amazing(self):
            return 'amazing!'

    return Class


s = new_class(str)('foo')
print(s)
print(s.amazing())

s = new_class(dict)()
print(s)
print(s.amazing())
