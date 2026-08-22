from typing import Any, Callable

_NONE = object()


class JsonL:
    def __init__(self):
        self._prev: dict[str, Any] = {'type': None}

    def __call__(self, d: dict[str, Any]) -> dict[str, Any]:
        res = self._call(d)
        self._prev = d
        return res

    def _call(self, d: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class CompressJsonL(JsonL):
    def _call(self, d: dict[str, Any]) -> dict[str, Any]:
        if self._prev['type'] != d['type']:
            return d
        return {k: v for k, v in d.items() if self._prev.get(k, _NONE) != v}


class DecompressJsonL(JsonL):
    def _call(self, d: dict[str, Any]) -> dict[str, Any]:
        return d if 'type' in d else d | self._prev
