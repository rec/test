import multiprocessing as mp


def run():
    procs = [mp.Process(target=print, args=('hello', i)) for i in range(4)]
    [p.start() for p in procs]


if __name__ == '__main__':
    print('main')
    run()
