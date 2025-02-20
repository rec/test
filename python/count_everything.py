import itertools
import json
import sys
import token
from pathlib import Path
from tokenize import generate_tokens, TokenInfo
from typing import Iterator
import dataclasses as dc


def _field(t: type) -> dc.field:
    return dc.field(default_factory=t)


@dataclass
class Line:
    line: str
    row: int
    column: int | None = None
    length: int | None = None


@dc.dataclass
class FileInfo:
    # These fields get filled in when we first see the file
    double_underscore_alls: list[Line] = field(list)
    type_ignores: dict[int, list[str]] = field(dict)
    blocks: list[Block] = field(list)
    outgoing_imports: list[str] = field(list)

    # This field gets filled in after we have seen all the files
    incoming_imports: dict[str, list[str]] = field(dict)



def all_python_files(path: str, prefix="", python_root=None):
    pass

if __name__ == '__main__':
     all_python_files(*sys.argv[1:])
