from dataclasses import dataclass


class ThreadQueue:
    maxsize = 1
    thread_count = 1
    callback = None
    thread = None

    def start(self):
        print(self.thread_count)


@dataclass(frozen=True)
class Desc:
    endpoints: tuple[str] = ()
    ip: str = '127.0.0.1'
    port: int = 5005
    maxsize: int = 0
    thread_count: int = 1

    def server(self):
        return BlockingOSCUDPServer(self.ip, self.port, self.dispatcher)


@dataclass(frozen=True)
class Server(Desc, ThreadQueue):
    callback: object

    def serve(self):
        pass


s = Server('callback', ('abc', 'def'), thread_count=2)
print(s)
s.start()
