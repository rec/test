class StoppableThread(threading.Thread):
    def __init__(self, target=None, *args, loop=None, daemon=True, **kwargs):
        super().__init__(*args, target=target, daemon=daemon, **kwargs)
        self.stopped_event = threading.Event()
        self._loop = loop or self._loop

    def stop(self):
        self.stopped_event.set()

    @property
    def running(self):
        return not self.stopped_event.is_set()

    def run(self):
        try:
            while self.running and self._target:
                self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs
