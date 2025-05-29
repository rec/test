from typing import Callable, Any

def a() -> int:
    return 1


def b(i: int) -> int:
    return i + 1


class A:
    def __call__(self, *args, **kwargs):
        return None

class B:
    def __call__(self, *args, **kwargs):
        return 1


s: set[Callable] = {a, b, print, A(), B()}
t: set[Callable[..., Any]] = {a, b, print, A(), B()}
u: set[Callable[..., Any]] = {a, b, print, A(), B(), None}
