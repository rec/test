from torch.utils._ordered_set import OrderedSet
from timeit import timeit


def time_in(container, item):
    return '{:6.2f}'.format(1000 * timeit(number=100_000, stmt=lambda: item in container))


print('|     i  |       set       |    OrderedSet   |      tuple      |')
print('|        |  hit   |  miss  |   hit  |  miss  |   hit  |  miss  |')

for i in (0, 1, 4, 8, 12, 16, 20, 64, 256):
    s = set(str(j) for j in range(i))
    os = OrderedSet(s)
    t = tuple(s)

    if i:
        middle = t[i // 2]
        hit_s = time_in(s, middle)
        hit_os = time_in(os, middle)
        hit_t = time_in(t, middle)
    else:
        hit_s = hit_os = hit_t = 6 * ' '

    missing = str(-1)
    miss_s = time_in(s, missing)
    miss_os = time_in(os, missing)
    miss_t = time_in(t, missing)

    print(f'|  {i:4}  | {hit_s} | {miss_s} | {hit_os} | {miss_os} | {hit_t} | {miss_t} |')
