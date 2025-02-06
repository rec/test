class Binary:
    def __eq__(self, other: int) -> "Binary":  # type: ignore[override]
        print("__eq__", other)
        return self

    def __ne__(self, other: int) -> "Binary":  # type: ignore[override]
        print("__ne__", other)
        return self

    def __lt__(self, other: int) -> "Binary":  # type: ignore[override]
        print("__lt__", other)
        return self

    def __le__(self, other: int) -> "Binary":  # type: ignore[override]
        print("__le__", other)
        return self


# from typing import assert_type
from typing_extensions import assert_type

assert_type(Binary() < 1, Binary)
assert_type(Binary() == 2, Binary)
assert_type(Binary() != 3, Binary)

assert_type(4 >= Binary(), bool)
assert_type(5 == Binary(), bool)
assert_type(6 != Binary(), bool)
