import inspect
from torch._dynamo.testing import standard_test


def make_test(fn):
    if fn is None:
        return lambda fn: make_test(fn, expected_frame_count=expected_frame_count)

    def test_fn():
        return standard_test(
            None,
            fn=fn,
            nargs=1,
            expected_frame_count=1,
        )

    return test_fn


@make_test
def test_dict_keys(x):
    d = {3: x}
    keys = d.keys()
    d[4] = x + 1
    d2 = {3: 2, 4: "aa"}
    return 3 in keys, 4 in keys, 5 in keys, d2.keys() == keys

test_dict_keys()
