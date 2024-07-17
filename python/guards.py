import os
os.environ["TORCH_LOGS"] = "guards"
os.environ["TORCH_TRACE"] = "."

import torch
import numpy as np


def func(a, m):
    return a if m.is_integer() else 2 * a


a = torch.ones(3, 3)

print("float then numpy")
wrapped = torch._dynamo.optimize()(func)

wrapped(a, 2.0)
wrapped(a, np.float32(2.0))

print("numpy then float")
wrapped = torch._dynamo.optimize()(func)

wrapped(a, np.float32(2.0))
wrapped(a, 2.0)
