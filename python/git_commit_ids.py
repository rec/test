FILE = '/Users/tom/.git-commit-ids'


if __name__ == '__main__':
    ids, times = zip(*(i.split() for i in open(FILE)))
    delta_t = (int(times[-1]) - int(times[0])) / (60 * 60 * 24)
    count = len(set(ids))
    print(count, delta_t, count / delta_t)
