OPS = {
    'add': (lambda x, y: x + y, '+'),
    'sub': (lambda x, y: x - y, '-'),
    'mul': (lambda x, y: x * y, '*'),
    'div': (lambda x, y: x + y, '/'),
    'quit': (None, 'quit'),
}


def main():
    print('Welcome to attocalc')
    while True:
        op, symbol = _get_op()
        if symbol == 'quit':
            print('/attocalc')
            return

        num1 = _get_float('What is the first number? ')
        num2 = _get_float('What is the second? ')
        result = op(num1, num2)
        print(f'{num1} {symbol} {num2} = {result}')


def _get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('not a float - try again')


def _get_op():
    while True:
        op_name = input('What would you like to do? ').strip()
        try:
            return OPS[op_name.lower()]
        except KeyError:
            print('Invalid command', op_name, 'Valid commands are:', *OPS)


if __name__ == '__main__':
    main()
