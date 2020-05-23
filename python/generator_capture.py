def run():
    def one():
        numbers = range(6)

        numbers = (i for i in numbers if i % 2)
        numbers = (i for i in numbers if i % 3)

        return numbers

    def two():
        numbers = range(6)

        for p in (2, 3):
            numbers = (i for i in numbers if i % p)

        return numbers

    print('one', *one())
    print('two', *two())


run()
