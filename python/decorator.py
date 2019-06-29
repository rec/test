def add_attrib(f):
    setattr(f, 'foo', True)
    return f

class Foo(object):
    @add_attrib
    def bar(self):
        pass
