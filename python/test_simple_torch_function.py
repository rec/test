import torch
import torch.nn.functional as F


@torch._dynamo.optimize(nopython=True)
def simple_function(x):
    # function call, twice to test wrapping
    x = F.sigmoid(x)
    x = F.sigmoid(x)
    # method call, twice to test wrapping
    x = x.sigmoid()
    x = x.sigmoid()
    return x


class TensorProxy(torch.Tensor):
    pass


torch._dynamo.config.traceable_tensor_subclasses.add(TensorProxy)
proxy = torch.randn(1)
simple_function(proxy)
