class Number:
    integer = 0

    def __index__(self):
        i = Number.integer
        Number.integer += 10
        return i

print(list(range(Number(), Number())))
