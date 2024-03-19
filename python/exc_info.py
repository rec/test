import sys

try:
    raise ValueError
finally:
    print(sys.exc_info())
