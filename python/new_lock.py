import threading


class Lock(threading.Lock):
    def acquire(self, blocking=True, timeout=-1):
        print('acquire')
        super().acquire(blocking, timeout)

    def release(self):
        print('release')
        super().release()


lock = Lock()

with lock:
    print('hello')
