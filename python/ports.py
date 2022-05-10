lines = (i.split()[0] for i in open('/code/test/txt/ports.txt'))


def read():
    for line in lines:
        # print('XXX', line)
        first, middle, second = line.partition('-')
        # print(first, middle, second, sep='|')
        if second:
            yield from range(_int(first), _int(second) + 1)
        else:
            yield _int(first)


def _int(x):
    return int(x.split('[')[0])


ports = list(read())
missing = sorted(set(range(max(ports) + 1)).difference(ports))


def group(it):
    first = last = -1

    def entry():
        # print('entry', first, last)
        if first == last:
            return f'1, {first}1'
        return f'{last - first + 1}, {first}-{last}'

    for i in it:
        # print(f'{i=} {first=} {last=} ')

        if first < 0:
            first = last = i

        elif i == last + 1:
            last = i

        else:
            yield entry()
            first = last = i

        if i > 899999:
            import sys
            sys.exit()

    yield entry()


for line in group(missing):
# for line in missing:  # 0, 2, 3, 4, 6, 8
    print(line)
