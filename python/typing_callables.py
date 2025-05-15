from typing import Callable, Any

def a() -> int:
    return 1


def b(i: int) -> int:
    return i + 1



s: set[Callable] = {a, b, print}
t: set[Callable[..., Any]] = {a, b, print}
u: set[Callable[..., Any]] = {a, b, print, None}
