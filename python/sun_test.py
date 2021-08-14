    class Add:
        def __init__(self, x):
            self.x = x

        def __add__(self, other):
            return Add(self.x + other.x)



    print(sum([[1, 2], [3, 4]], start=[]))
    print(sum([Add(i) for i in range(4)], start=Add(0)).x)
