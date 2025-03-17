from __future__ import annotations

from typing import Any, Type, Generic, get_args, TypeVar
T = TypeVar('T')


class NameableType(Generic[T]):
    @classmethod
    def type(cls) -> Type[T]:
        return get_args(cls.__orig_bases__[0])[0]


class StrType(NameableType[str]):
    pass


class IntType(NameableType[int]):
    pass


print(StrType.type(), IntType.type())
