import torch
import torch.nn.functional as F


@torch._dynamo.optimize(nopython=True)
def simple_function(x):
    x = torch.abs(x)
    return x.abs()


class TensorProxy(torch.Tensor):
    pass


torch._dynamo.config.traceable_tensor_subclasses.add(TensorProxy)
proxy = torch.randn(1).as_subclass(TensorProxy)
simple_function(proxy)
