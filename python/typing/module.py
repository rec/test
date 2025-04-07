from typing import Any
from typing_extensions import assert_type


class Module:
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._implementation(*args, **kwargs)

    def _implementation(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class Imp(Module):
    def _implementaion(self, name: str = "name", *, value: int = 0) -> str:
        return f"{name}={value}"


imp = Imp()
a = imp()
b = imp._implementaion()

assert_type(a, Any)
assert_type(b, str)
assert_type(a, str)
