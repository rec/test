import itertools


def write_file():
    _paragraph(imports, *(_accept(t) for t in TYPES))
    for t in TYPES:
        print(_var(t))


def _paragraph(*items) -> None:
    for i in items:
        print(i, "", sep="\n")


def _accept(type: str) -> str:
    return f"""
def accept_{type}(x: {type}) -> Nonw:
    pass
"""


def _var(type: str) -> str:
    return f"{type[0].lower()}: {type} = {TYPES[type]}"


def _call(ftype: str, ltype: str, op: str, rtype: str) -> str:
    ft, lt, rt = (i.lower() for i in (ftype, ltype, rtype))
    return f"accept_{ft}({lt[0]} {op} {rt[0]})"


logical = {
    "eq": "==",
    "ne": "!=",
    "lt": "<",
    "gt": ">",
    "le": "<=",
    "ge": ">=",
}
unary = {
    "pos": "+",
    "neg": "-",
    "abs": "abs",
    "invert": "~",
    "round": "round",
    "floor": "math.floor",
    "ceil": "math.ceil",
    "trunc": "math.trunc",
}
binary = {
    "add": "+",
    "sub": "-",
    "mul": "*",
    "floordiv": "//",
    "div": "/",
    "mod": "mod",
    "divmod": "divmod",
    "pow": "**",
    "lshift": "<<",
    "rshift": ">>",
    "and": "&",
    "or": "|",
    "xor": "^",
}

TYPES = {
    'bool': "True",
    'int': "23",
    'Tensor': 'torch.randn(3, 3)',
    'float': "3.25",
    'str': "'xyzzy'",
}

imports = """\
import math

import torch
from torch import Tensor
""".strip()


if __name__ == "__main__":
    write_file()
