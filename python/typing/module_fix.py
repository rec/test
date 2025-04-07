from typing import Any
from typing_extensions import assert_type
import functools


class Module:
    def _implementation(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    def __init_subclass__(cls) -> None:
        @functools.wraps(cls._implementation)
        def __call__(self, *a: Any, **ka: Any) -> Any:
            return self._implementation(*a, **ka)

        cls.__call__ = __call__  # type: ignore[method-assign]


class Imp(Module):
    def _implementation(self, name: str = "name", *, value: int = 0) -> str:
        return f"{name}={value}"


imp = Imp()
a = imp()
b = imp._implementation()

assert_type(a, Any)
assert_type(b, str)
assert_type(a, str)
