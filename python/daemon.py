import time, threading


def target():
    print('start')
    time.sleep(10)
    print('end')


def run():
    print('running')
    threading.Thread(target=target, daemon=True).start()
    time.sleep(1)
    print('ran')


run()
