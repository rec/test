import sys, time, requests, random
import itertools


def main():
    for c in itertools.count():
        if not (c % 40):
            print()
        print('-', end='')
        sys.stdout.flush()
        try:
            requests.get(sys.argv[1])
        except Exception:
            print('!', end='')
        else:
            print('.', end='')
        sys.stdout.flush()
        while (t := random.gauss(3, 1.5)) < 0:
            pass
        time.sleep(t)

if __name__ == '__main__':
    main()
