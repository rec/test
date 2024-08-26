import torch
import random


@torch._dynamo.optimize(nopython=True)
def simple_function(rand2):
    return rand2.randint(1, 9)


simple_function(random.Random(12))
