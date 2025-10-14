def it():
    i = iter(range(4))
    while True:
        yield next(i)


print(*it())
