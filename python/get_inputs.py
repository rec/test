def get_float(prompt):
    while True:
        f = input(prompt + ': ')
        try:
            return float(f)
        except Exception:
            print(f'"{f}" cannot be converted to a number. Try again!')


x = get_float('Enter x')
y = get_float('Enter y')
print(f'The product of {x} and {y} is {x * y}.')
