import timeit
N = 10000000

def a():
    return [i + 4 for i in range(N)]


def b():
    x = []
    for i in range(N):
        x.append(i + 4)
    return x

print(timeit.timeit(a, number=1))
print(timeit.timeit(b, number=1))
