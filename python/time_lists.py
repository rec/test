#!/usr/bin/env python3

import sys, timeit

def run_timer(length=100000, number=100):
    return timeit.timeit('sum(range(%s))' % int(length), number=int(number))

print(run_timer(*sys.argv[1:]))

"""
$ ./time_lists.py 1000000 100
2.0413582772016525

$ ./time_lists.py 100000 100
0.21472625294700265

$ ./time_lists.py 10000 100
0.01866426272317767

$ ./time_lists.py 100000 1000
2.1271090572699904

"""
