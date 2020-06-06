from subprocess import Popen, PIPE
from threading import Thread

SHELL = False
CMD = ['/bin/bash', '-i']
# CMD = ['/usr/local/bin/python3.7', '-i']


def main():
    sub = Popen(CMD, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf8')

    def new_thread(stream, prefix):
        def read():
            line = '.'
            while line or sub.poll() is None:
                line = stream.readline().rstrip('\n')
                print(prefix, line)

        thread = Thread(target=read, daemon=True)
        thread.start()
        return thread

    new_thread(sub.stdout, '.')
    new_thread(sub.stderr, '!')

    while True:
        s = input(': ')
        if s:
            sub.stdin.write(s + '\n')
            sub.stdin.flush()
        else:
            break


if __name__ == '__main__':
    main()
