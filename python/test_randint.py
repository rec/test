import torch
import random


@torch._dynamo.optimize(nopython=True)
def simple_function(rand2):
    r1 = random.randint(1, 9)
    r2 = rand2.randint(1, 9)
    return r1, r2


simple_function(random.Random(12))
