import torch
import torch.nn.functional as F


@torch._dynamo.optimize(nopython=True)
def simple_function(x):
    return F.sigmoid(x)


class TensorProxy(torch.Tensor):
    @classmethod
    def __torch_function__(cls, func, types, args=(), kwargs=None):
        return super().__torch_function__(func, types, args, kwargs)


torch._dynamo.config.traceable_tensor_subclasses.add(TensorProxy)
proxy = torch.randn(1).as_subclass(TensorProxy)
simple_function(proxy)
