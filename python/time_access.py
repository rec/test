from torch.utils._ordered_set import OrderedSet
from timeit import timeit


def time_in(container, item):
    return '{:6.2f}'.format(1000 * timeit(number=100_000, stmt=lambda: item in container))


print('|     i  |       set       |      tuple      |    OrderedSet   |')
print('|        |  hit   |  miss  |   hit  |  miss  |   hit  |  miss  |')

for i in (0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 64, 256):
    s = set(str(j) for j in range(i))
    os = OrderedSet(str(j) for j in range(i))
    t = tuple(s)
    missing = str(-1)

    if i:
        middle = t[i // 2]
        hit_t = time_in(t, middle)
        hit_s = time_in(s, middle)
        hit_os = time_in(os, middle)
    else:
        hit_t = hit_s = hit_os = 6 * ' '

    miss_s = time_in(s, missing)
    miss_t = time_in(t, missing)
    miss_os = time_in(os, missing)

    print(f'|  {i:4}  | {hit_s} | {miss_s} | {hit_t} | {miss_t} | {hit_os} | {miss_os} |')
