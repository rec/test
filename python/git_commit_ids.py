FILE = '/Users/tom/.git-commit-ids'


if __name__ == '__main__':
    ids, times = [], []

    for i, line in enumerate(open(FILE)):
        try:
            id, time = line.split()
        except ValueError:
            print('Bad line %d: "%s"' % (i, line[:-1]))
        else:
            ids.append(id)
            times.append(time)

    days = (int(times[-1]) - int(times[0])) / (60 * 60 * 24)
    count = len(set(ids))
    print('count =', count, 'days =', days, 'commits/day =', count / days)
