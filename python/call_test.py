class Call1(object):
    def __call__(self, x):
        return x

class Call2(object):
    def __init__(self):
        self.call = lambda x: x

    def __call__(self, x):
        return self.call(x)

class Call3(object):
    def __init__(self):
        self.__call__ = lambda x: x


print(Call1()(3))
print(Call2()(3))
print(Call3()(3))
