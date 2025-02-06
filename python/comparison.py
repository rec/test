from typing_extensions import assert_type


class Test:
    def __eq__(self, other: int) -> "Test":  # type: ignore[override]
        print("__eq__", self, other)
        return self

    def __ne__(self, other: int) -> "Test":  # type: ignore[override]
        print("__ne__", self, other)
        return self

    def __lt__(self, other: int) -> "Test":  # type: ignore[override]
        print("__lt__", self, other)
        return self

    def __gt__(self, other: int) -> "Test":  # type: ignore[override]
        print("__gt__", self, other)
        return self

    def __le__(self, other: int) -> "Test":  # type: ignore[override]
        print("__le__", self, other)
        return self

    def __ge__(self, other: int) -> "Test":  # type: ignore[override]
        print("__ge__", self, other)
        return self


assert_type(Test() < 1, Test)
assert_type(1 >= Test(), Test)
