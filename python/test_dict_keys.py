import inspect
from torch._dynamo.testing import standard_test


def make_test(fn=None, expected_frame_count=1):
    if fn is None:
        return lambda fn: make_test(fn, expected_frame_count=expected_frame_count)

    nargs = len(inspect.signature(fn).parameters)

    def test_fn(self):
        return standard_test(
            self,
            fn=fn,
            nargs=nargs,
            expected_frame_count=expected_frame_count,
        )

    return test_fn


@make_test
def test_dict_keys(x):
    d = {3: x}
    keys = d.keys()
    d[4] = x + 1
    d2 = {3: 2, 4: "aa"}
    return 3 in keys, 4 in keys, 5 in keys, d2.keys() == keys

test_dict_keys(None)
