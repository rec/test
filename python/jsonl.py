from typing import Any, Callable
from copy import deepcopy

_NONE = object()


class Jsonl:
    def __init__(self) -> None:
        self._types: dict[str, dict[str, Any]] = {}

    def _call(self, d: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def __call__(self, it: Iterable[dict[str, Any]]) -> Iterator[dict[str, Any]]:
        yield from (self._call(i) for i in it)


class Decompress(Jsonl):
    def _call(self, d: dict[str, Any]) -> dict[str, Any]:
        prev = self._types.setdefault(d['type'], {})
        res = prev | d
        prev.update(d)
        return res


class Compress(Jsonl):
    def _call(self, d: dict[str, Any]) -> dict[str, Any]:
        prev = self._types.setdefault(d['type'], {})

        def accept(k: str, v: Any) -> bool:
            return k == 'type' or prev.get(k, _NONE) != v

        return {k: v for k, v in b.items() if accept(k, v)}
