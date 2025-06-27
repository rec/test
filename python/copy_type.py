from abc import ABC, abstractmethod
from typing import Any, TypeVar, Callable
from typing_extensions import override, reveal_type


_T = TypeVar("_T")


class Module(ABC):
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.forward(*args, **kwargs)

    @abstractmethod
    def forward(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


def copy_type(f: _T) -> Callable[[Any], _T]:
    # From https://github.com/python/typing/issues/769#issuecomment-903760354
    return lambda x: x


class Implementation(Module):
    @override
    def forward(self, x: int, /, y: str) -> int:
        return x * int(y)

    # This boilerplate would need to be pasted into any class derived from Module
    # to get the right typing for `__call__`
    @copy_type(forward)
    def __call__(self, *a: Any, **k: Any) -> Any:
        return super().__call__(*a, **k)


imp = Implementation()
print(imp(2, "3"))
print(imp("2", "3"))

# mypy says:
# copy_type.py:34: error: Argument 1 to "__call__" of "Implementation" has incompatible type "str"; expected "int"  [arg-type]
# Found 1 error in 1 file (checked 1 source file)
