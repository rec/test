import os
import sys
import time
from watchdog.observers import Observer
from tempfile import TemporaryDirectory

USE_TEMP = not False


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    class event_handler:
        @staticmethod
        def dispatch(event):
            print(event)

    with TemporaryDirectory() as td:
        master = os.path.join(td, '_master')
        os.mkdir(master)
        observer = Observer()

        d = os.path.abspath(master if USE_TEMP else path)
        print('watching', d)
        observer.schedule(event_handler, d, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
