import torch
from torch._dynamo import testing, eval_frame
from torch._dynamo.eval_frame import optimize_assert

def test_dict_keys(x):
    d = {3: x}
    keys = d.keys()
    d[4] = x + 1
    d2 = {3: 2, 4: "aa"}
    return 3 in keys, 4 in keys, 5 in keys, d2.keys() == keys

actual = testing.CompileCounter()
optimize = optimize_assert(actual)

if True:
    optimize = torch._dynamo.optimize(nopython=True)

args1 = [torch.randn(10, 10)]
opt_fn = optimize(test_dict_keys)
val1a = opt_fn(*args1)
