from typing import Any
from typing_extensions import assert_type
import functools


class Module:
    def _implementation(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class Meta(type):
    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]) -> type:
        @functools.wraps(attrs["_implementation"])
        def __call__(self, *a: Any, **ka: Any) -> Any:
            return self._implementation(*a, **ka)

        attrs["__call__"] = __call__
        return super().__new__(cls, name, bases, attrs)


class Imp(Module, metaclass=Meta):
    def _implementation(self, name: str = "name", *, value: int = 0) -> str:
        return f"{name}={value}"


imp = Imp()
a = imp()
b = imp._implementation()

assert_type(a, Any)
assert_type(b, str)
assert_type(a, str)
