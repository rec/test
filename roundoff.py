import numpy as np

def diffs():
    a = np.random.rand(4,4) # may need to try a few random calls
    a_f = np.fft.fft2(a)
    a_prime = np.fft.ifft2(a_f)
    return np.ma - a_prime)

for i in range(1000):
