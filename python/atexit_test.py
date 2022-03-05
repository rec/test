from threading import Thread
import atexit
import time


def run():
    atexit.register(print, 'atexit!')

    Thread(target=loop, args=('one', 1, 3)).start()
    Thread(target=loop, args=('two', 1.01), daemon=True).start()
    time.sleep(2)
    print('END')
    import traceback
    traceback.print_stack()


def loop(name, t, r=10):
    for i in range(r):
        time.sleep(t)
        print(name, i)


run()
