class HasLen:
    def __init__(self, i):
        self.i = i

    def __len__(self):
        return self.i


print(bool(HasLen(0)), bool(HasLen(1)))
