def sqrt(x, precision=1E-10):
    last_guess = x
    guess = x / 2
    iterations = 0
    while abs(last_guess - guess) >= precision:
        last_guess = guess
        guess = ((x / guess) + guess) / 2
        iterations += 1

    print(iterations)
    return guess

print(sqrt(2000000))
