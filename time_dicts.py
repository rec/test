#!/usr/bin/env python3

import timeit

NUMBER = 100000

print(timeit.timeit('dict(a=1, b=2)', number=NUMBER))
print(timeit.timeit('{"a": 1, "b": 2}', number=NUMBER))
