import torch
# import torch.nn.functional as F
import os


def env(name):
    return int(os.environ.get('TEST_' + name, '0'))


COMPILE = env('COMPILE')
LATE_SUBCLASS = env('LATE_SUBCLASS')
NO_SUBCLASS = env('NO_SUBCLASS')
TWO_SIGS = env('TWO_SIGS')
TORCH_FUNCTION = env('TORCH_FUNCTION')
ALLOW_BREAKS = env('ALLOW_BREAKS')

print('\n', *(f'{k}={v}' for k, v in globals().items() if k.isupper()), '\n')


class TensorSubclass(torch.Tensor):
    if TORCH_FUNCTION:
        @classmethod
        def __torch_function__(cls, func, types, args=(), kwargs=None):
            return super().__torch_function__(func, types, args, kwargs)


if LATE_SUBCLASS:
    if TWO_SIGS:
        def simple_function(x):
            x = x.as_subclass(TensorSubclass)
            x = x.sigmoid()
            return x.sigmoid()
    else:
        def simple_function(x):
            x = x.as_subclass(TensorSubclass)
            return x.sigmoid()

else:
    if TWO_SIGS:
        def simple_function(x):
            x = x.sigmoid()
            return x.sigmoid()
    else:
        def simple_function(x):
            return x.sigmoid()

if COMPILE:
    simple_function = torch.compile(fullgraph=not ALLOW_BREAKS)(simple_function)
else:
    simple_function = torch._dynamo.optimize(nopython=not ALLOW_BREAKS)(simple_function)

torch._dynamo.config.traceable_tensor_subclasses.add(TensorSubclass)
x = torch.randn(1)
if not NO_SUBCLASS:
    x = x.as_subclass(TensorSubclass)
simple_function(x)
