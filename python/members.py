import inspect


class C:
    @staticmethod
    def static(self):
        pass

    @classmethod
    def cmethod(cls, self):
        pass

    def method(self):
        pass

    @property
    def prop(self):
        pass


def run():
    items = C.static, C.method, C.method, C.prop
    for k, v in vars(inspect).items():
        if k.startswith('is') and callable(v):
            print(*(' x'[v(i)] for i in items), k)

run()
