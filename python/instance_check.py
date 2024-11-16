class NotDict(dict):
    @classmethod
    def __instancecheck__(cls, instance):
        assert False


d = NotDict()
print(isinstance(d, dict))
