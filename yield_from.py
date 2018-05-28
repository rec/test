def test():
    yield 2
    yield from range(4)
    yield from zip(range(3), range(3))

print(list(test()))
