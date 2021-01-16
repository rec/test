import numpy as np

a = np.ones(shape=(3, 2), dtype=np.uint16)
b = np.ones(shape=(3, 2))
b += a
print(b)
