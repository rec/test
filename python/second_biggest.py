MINUS_INF = -float('inf')


def second_biggest(items):
    bigger = biggest = MINUS_INF

    for i in items:
        if i > biggest:
            bigger = biggest
            biggest = i
        elif biggest > i > bigger:
            bigger = i

    return bigger


assert second_biggest([]) == MINUS_INF
assert second_biggest([3]) == MINUS_INF
assert second_biggest([3, 3]) == MINUS_INF
assert second_biggest([3, 3, 3]) == MINUS_INF
assert second_biggest([3, 2, 3]) == 2
