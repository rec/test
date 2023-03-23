def func():
    print('Function part 1')

    x = yield 'a'
    print(x)
    print('Function part 2')

    a = yield 'b'
    print(a)
    print('Function part 3')


try:

    y = func()

    print(next(y))	        # Function part 1 executed, to reach the first yield we used next

    # y.send(6)		# Function part 2 executed and value sent 6
    print(y.send(12))		# Function part 2 executed and value sent 12 and StopIteration raised
    print(next(y))
except StopIteration as e:
    pass
