class Iter:
    def __iter__(self):
        for i in range(3):
            yield str(i), i


print(*Iter())
