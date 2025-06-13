from __future__ import annotations

from typing import Any, Generic, TypeVar, cast, get_args

DataType = TypeVar("DataType")


class TypeNamer(Generic[DataType]):
    pass


class Time(TypeNamer["Time"]):
    pass


print(Time())
