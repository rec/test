from typing import Any
from typing_extensions import assert_type

from torch import randn, Tensor


TENSOR, INT, FLOAT, BOOL = randn(3), 2, 1.5, True

# Test deduced types of arithmetic operations between tensors, ints, floats and bools
# The expected type should always be `Tensor`: `Any` and `bool` below are wrong.
# See https://github.com/pytorch/pytorch/issues/145838

# Unary ops

assert_type(+TENSOR, Tensor)
assert_type(-TENSOR, Tensor)
assert_type(~TENSOR, Tensor)

# Binary ops

assert_type(TENSOR == TENSOR, Tensor)
assert_type(TENSOR != TENSOR, Tensor)
assert_type(TENSOR < TENSOR, Tensor)
assert_type(TENSOR > TENSOR, Tensor)
assert_type(TENSOR <= TENSOR, Tensor)
assert_type(TENSOR >= TENSOR, Tensor)
assert_type(TENSOR + TENSOR, Tensor)
assert_type(TENSOR - TENSOR, Tensor)
assert_type(TENSOR * TENSOR, Tensor)
assert_type(TENSOR // TENSOR, Any)
assert_type(TENSOR / TENSOR, Tensor)
assert_type(TENSOR % TENSOR, Tensor)
assert_type(TENSOR**TENSOR, Any)
assert_type(TENSOR << TENSOR, Tensor)
assert_type(TENSOR >> TENSOR, Tensor)
assert_type(TENSOR & TENSOR, Tensor)
assert_type(TENSOR | TENSOR, Tensor)
assert_type(TENSOR ^ TENSOR, Tensor)

assert_type(TENSOR == BOOL, Tensor)
assert_type(TENSOR != BOOL, Tensor)
assert_type(TENSOR < BOOL, Tensor)
assert_type(TENSOR > BOOL, Tensor)
assert_type(TENSOR <= BOOL, Tensor)
assert_type(TENSOR >= BOOL, Tensor)
assert_type(TENSOR + BOOL, Tensor)
assert_type(TENSOR - BOOL, Tensor)
assert_type(TENSOR * BOOL, Tensor)
assert_type(TENSOR // BOOL, Any)
assert_type(TENSOR / BOOL, Tensor)
assert_type(TENSOR % BOOL, Tensor)
assert_type(TENSOR**BOOL, Any)
assert_type(TENSOR << BOOL, Tensor)
assert_type(TENSOR >> BOOL, Tensor)
assert_type(TENSOR & BOOL, Tensor)
assert_type(TENSOR | BOOL, Tensor)
assert_type(TENSOR ^ BOOL, Tensor)

assert_type(BOOL == TENSOR, bool)
assert_type(BOOL != TENSOR, bool)
assert_type(BOOL < TENSOR, Tensor)
assert_type(BOOL > TENSOR, Tensor)
assert_type(BOOL <= TENSOR, Tensor)
assert_type(BOOL >= TENSOR, Tensor)
assert_type(BOOL + TENSOR, Tensor)
assert_type(BOOL - TENSOR, Any)
assert_type(BOOL * TENSOR, Tensor)
assert_type(BOOL // TENSOR, Any)
assert_type(BOOL / TENSOR, Any)
assert_type(BOOL % TENSOR, Any)
assert_type(BOOL**TENSOR, Any)
assert_type(BOOL << TENSOR, Any)
assert_type(BOOL >> TENSOR, Any)
assert_type(BOOL & TENSOR, Tensor)
assert_type(BOOL | TENSOR, Tensor)
assert_type(BOOL ^ TENSOR, Tensor)

assert_type(TENSOR == INT, Tensor)
assert_type(TENSOR != INT, Tensor)
assert_type(TENSOR < INT, Tensor)
assert_type(TENSOR > INT, Tensor)
assert_type(TENSOR <= INT, Tensor)
assert_type(TENSOR >= INT, Tensor)
assert_type(TENSOR + INT, Tensor)
assert_type(TENSOR - INT, Tensor)
assert_type(TENSOR * INT, Tensor)
assert_type(TENSOR // INT, Any)
assert_type(TENSOR / INT, Tensor)
assert_type(TENSOR % INT, Tensor)
assert_type(TENSOR**INT, Any)
assert_type(TENSOR << INT, Tensor)
assert_type(TENSOR >> INT, Tensor)
assert_type(TENSOR & INT, Tensor)
assert_type(TENSOR | INT, Tensor)
assert_type(TENSOR ^ INT, Tensor)

assert_type(INT == TENSOR, bool)
assert_type(INT != TENSOR, bool)
assert_type(INT < TENSOR, Tensor)
assert_type(INT > TENSOR, Tensor)
assert_type(INT <= TENSOR, Tensor)
assert_type(INT >= TENSOR, Tensor)
assert_type(INT + TENSOR, Tensor)
assert_type(INT - TENSOR, Any)
assert_type(INT * TENSOR, Tensor)
assert_type(INT // TENSOR, Any)
assert_type(INT / TENSOR, Any)
assert_type(INT % TENSOR, Any)
assert_type(INT**TENSOR, Any)
assert_type(INT << TENSOR, Any)
assert_type(INT >> TENSOR, Any)
assert_type(INT & TENSOR, Any)  # type: ignore[operator]
assert_type(INT | TENSOR, Any)  # type: ignore[operator]
assert_type(INT ^ TENSOR, Any)  # type: ignore[operator]

assert_type(TENSOR == FLOAT, Tensor)
assert_type(TENSOR != FLOAT, Tensor)
assert_type(TENSOR < FLOAT, Tensor)
assert_type(TENSOR > FLOAT, Tensor)
assert_type(TENSOR <= FLOAT, Tensor)
assert_type(TENSOR >= FLOAT, Tensor)
assert_type(TENSOR + FLOAT, Tensor)
assert_type(TENSOR - FLOAT, Tensor)
assert_type(TENSOR * FLOAT, Tensor)
assert_type(TENSOR // FLOAT, Any)
assert_type(TENSOR / FLOAT, Tensor)
assert_type(TENSOR % FLOAT, Tensor)
assert_type(TENSOR**FLOAT, Any)
assert_type(TENSOR << FLOAT, Tensor)
assert_type(TENSOR >> FLOAT, Tensor)
assert_type(TENSOR & FLOAT, Tensor)
assert_type(TENSOR | FLOAT, Tensor)
assert_type(TENSOR ^ FLOAT, Tensor)

assert_type(FLOAT == TENSOR, bool)
assert_type(FLOAT != TENSOR, bool)
assert_type(FLOAT < TENSOR, Tensor)
assert_type(FLOAT > TENSOR, Tensor)
assert_type(FLOAT <= TENSOR, Tensor)
assert_type(FLOAT >= TENSOR, Tensor)
assert_type(FLOAT + TENSOR, Tensor)
assert_type(FLOAT - TENSOR, Any)
assert_type(FLOAT * TENSOR, Tensor)
assert_type(FLOAT // TENSOR, Any)
assert_type(FLOAT / TENSOR, Any)
assert_type(FLOAT % TENSOR, Any)
assert_type(FLOAT**TENSOR, Any)
assert_type(FLOAT << TENSOR, Any)
assert_type(FLOAT >> TENSOR, Any)
assert_type(FLOAT & TENSOR, Tensor)  # type: ignore[operator]
assert_type(FLOAT | TENSOR, Tensor)  # type: ignore[operator]
assert_type(FLOAT ^ TENSOR, Tensor)  # type: ignore[operator]


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
