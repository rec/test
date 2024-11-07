from timeit import timeit


def time_in(container, item):
    return '{:7.2f}'.format(1000 * timeit(lambda: item in container))


for i in (0, 4, 16, 64, 256, 1024, 4096, 16384, 65536):
    s = {str(i) for j in range(i)}
    t = tuple(s)
    missing = str(-1)

    if i:
        middle = t[i // 2]
        hit_t = time_in(t, middle)
        hit_s = time_in(s, middle)
    else:
        hit_t = hit_s = 7 * ' '

    miss_s = time_in(s, missing)
    miss_t = time_in(t, missing)

    print('|    i    |      set       |     tuple      |')
    print('|         |  hit  |  miss  |  hit  |  miss  |')
    print(f'| {i:7} | {hit_s} | {miss_s} | {hit_t} {miss_t}')
