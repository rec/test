import os
os.environ["TORCH_LOGS"] = "guards"
os.environ["TORCH_TRACE"] = "."

import torch
import numpy as np


@torch._dynamo.optimize()
def func1(a, m):
    return a if m.is_integer() else 2 * a


@torch._dynamo.optimize()
def func2(a, m):
    return a if m.is_integer() else 2 * a


a = torch.ones(3, 3)

print("float then numpy")

func1(a, 2.0)
func1(a, np.float32(2.0))

print("numpy then float")

func2(a, np.float32(2.0))
func2(a, 2.0)
