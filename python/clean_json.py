import json
from typing import Any, Iterator


INDENT = 4


def clean_json(obj: Any, *, indent: int | None = None, **kwargs: Any) -> str:
    """Multi-line JSON but which fits lists and dicts of scalars onto one line"""
    delta = " " * (indent or INDENT)

    def to_json(x: Any, total_indent: str = "") -> Iterator[str]:
        items: Iterator[tuple[str, Any]]

        if isinstance(x, dict) and any(isinstance(i, dict) for i in x.values()):
            opener, closer = "{", "}"
            items = iter(x.items())
            key_format = '"{key}": '.format
        elif isinstance(x, list) and any(isinstance(i, dict) for i in x):
            opener, closer = "[", "]"
            items = (("", i) for i in x)
            key_format = "".format
        else:
            yield json.dumps(x, **kwargs)
            return

        yield opener
        yield "\n"

        next_indent = total_indent + delta
        for i, (k, v) in enumerate(items):
            yield next_indent
            yield key_format(key=k)
            yield from to_json(v, next_indent)
            if i != len(x) - 1:
                yield ","
            yield "\n"

        yield total_indent
        yield closer
        if not total_indent:
            yield "\n"

    return "".join(to_json(obj))
