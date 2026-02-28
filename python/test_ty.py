t, u = tuple(range(2))

reveal_type(t)
reveal_type(t[:2])

a: tuple[int, int] = t[:1]
b: tuple[int, int] = t[:2]
c: tuple[int, int] = t[:]

assert len(t) == 2
c: tuple[int, int] = t
