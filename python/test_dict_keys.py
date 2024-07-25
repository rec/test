import torch
from torch._dynamo import testing, eval_frame
from torch._dynamo.eval_frame import optimize_assert

@torch._dynamo.optimize(nopython=True)
def test_dict_keys(x):
    return {}.keys() == {}.keys()

test_dict_keys(torch.randn(10, 10))
