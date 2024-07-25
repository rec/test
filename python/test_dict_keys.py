import torch
from torch._dynamo import testing, eval_frame
from torch._dynamo.eval_frame import optimize_assert

@torch._dynamo.optimize(nopython=True)
def test_dict_keys(x):
    d = {3: x}
    keys = d.keys()
    d[4] = x + 1
    d2 = {3: 2, 4: "aa"}
    return d2.keys() == keys

test_dict_keys(torch.randn(10, 10))
