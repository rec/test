import torch
from torch._dynamo import testing, eval_frame

def standard_test(fn):
    actual = testing.CompileCounter()

    args1 = [torch.randn(10, 10)]
    args2 = [torch.randn(10, 10)]
    correct1 = fn(*args1)
    correct2 = fn(*args2)
    opt_fn = eval_frame.optimize_assert(actual)(fn)
    val1a = opt_fn(*args1)
    val2a = opt_fn(*args2)
    val1b = opt_fn(*args1)
    val2b = opt_fn(*args2)


def make_test(fn):
    def test_fn():
        return standard_test(fn)

    return test_fn


@make_test
def test_dict_keys(x):
    d = {3: x}
    keys = d.keys()
    d[4] = x + 1
    d2 = {3: 2, 4: "aa"}
    return 3 in keys, 4 in keys, 5 in keys, d2.keys() == keys

test_dict_keys()
