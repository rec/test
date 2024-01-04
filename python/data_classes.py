from dataclasses import dataclass
import timeit
import typing as t


@dataclass
class NormalData:
    a: int
    b: int
    c: int


@dataclass(frozen=True)
class FrozenData:
    a: int
    b: int
    c: int



class TupleData(t.NamedTuple):
    a: int
    b: int
    c: int


# Measure instantiation time for NormalData
normal_time = timeit.timeit(lambda: NormalData(1, 2, 3), number=1_000_000)

# Measure instantiation time for FrozenData
frozen_time = timeit.timeit(lambda: FrozenData(1, 2, 3), number=1_000_000)

# Measure instantiation time for TupleData
tuple_time = timeit.timeit(lambda: TupleData(1, 2, 3), number=1_000_000)

print(f"Normal data class: {normal_time}")
print(f"Frozen data class: {frozen_time}")
print(f"Tuple data class: {tuple_time}")
print(f"Frozen data class is {frozen_time / normal_time}x slower")
print(f"Tuple data class is {tuple_time / normal_time}x slower")
