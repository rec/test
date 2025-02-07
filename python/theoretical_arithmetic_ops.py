class Binary:
    def __add__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __and__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __ceil__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __cmp__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __div__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __divmod__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __eq__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __floor__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __floordiv__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __ge__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __gt__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __iadd__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __iand__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __idiv__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __idivmod__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __ifloordiv__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __ilshift__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __imod__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __imul__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __invert__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __ior__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __ipow__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __irshift__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __isub__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __itruediv__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __ixor__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __le__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __lshift__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __lt__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __mod__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __mul__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __ne__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __or__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __pow__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __radd__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __rand__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __rdiv__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __rdivmod__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __rfloordiv__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __rlshift__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __rmod__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __rmul__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __ror__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __round__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __rpow__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __rrshift__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __rshift__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __rsub__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __rtruediv__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __rxor__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __sub__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __truediv__(self, other: int) -> "Binary":  # type: ignore[override]
        return self

    def __xor__(self, other: int) -> "Binary":  # type: ignore[override]
        return self


from typing_extensions import assert_type

assert_type(Binary() + 5, Binary)
assert_type(Binary() & 5, Binary)
assert_type(Binary() / 5, Binary)
assert_type(Binary() == 5, Binary)
assert_type(Binary() // 5, Binary)
assert_type(Binary() >= 5, Binary)
assert_type(Binary() > 5, Binary)
assert_type(Binary() <= 5, Binary)
assert_type(Binary() << 5, Binary)
assert_type(Binary() < 5, Binary)
assert_type(Binary() % 5, Binary)
assert_type(Binary() * 5, Binary)
assert_type(Binary() != 5, Binary)
assert_type(Binary() | 5, Binary)
assert_type(Binary()**5, Binary)
assert_type(Binary() >> 5, Binary)
assert_type(Binary() - 5, Binary)
assert_type(Binary() ^ 5, Binary)

assert_type(5 + Binary(), Binary)
assert_type(5 & Binary(), Binary)
assert_type(5 / Binary(), Binary)
assert_type(5 == Binary(), bool)
assert_type(5 // Binary(), Binary)
assert_type(5 >= Binary(), Binary)
assert_type(5 > Binary(), Binary)
assert_type(5 <= Binary(), Binary)
assert_type(5 << Binary(), Binary)
assert_type(5 < Binary(), Binary)
assert_type(5 % Binary(), Binary)
assert_type(5 * Binary(), Binary)
assert_type(5 != Binary(), bool)
assert_type(5 | Binary(), Binary)
assert_type(5**Binary(), Binary)
assert_type(5 >> Binary(), Binary)
assert_type(5 - Binary(), Binary)
assert_type(5 ^ Binary(), Binary)
