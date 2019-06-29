import signal, time

STATE = 0

def state2(signum, frame):
    print('state2')
    signal.signal(signal.SIGHUP, signal.SIG_DFL)


def state1(signum, frame):
    print('state1')
    signal.signal(signal.SIGHUP, state2)


signal.signal(signal.SIGHUP, state1)
while STATE < 10:
    time.sleep(0.01)
