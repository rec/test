from enum import Enum

class E(Enum):
    a = 1
    b = 2 * a
    c = 2 * b


print(E.a, E.b, E.c)
