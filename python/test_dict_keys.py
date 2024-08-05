import torch

@torch._dynamo.optimize(nopython=True)
def test_dict_keys(x):
    return {}.keys()

test_dict_keys(torch.randn(10, 10))
