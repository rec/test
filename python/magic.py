import itertools


def write_file():
    def var(type: str) -> str:
        return f"{type[0].lower()}: {type} = {TYPES[type]}"

    def unary(ftype: str, op: str, rtype: str) -> str:
        ftype, rtype = (i.lower() for i in (ftype, rtype))
        if len(op) == 1:
            return f"accept_{ftype}({op}{rtype[0]})"
        else:
            return f"accept_{ftype}({op}({rtype[0]}))"

    def binary(ftype: str, ltype: str, op: str, rtype: str) -> str:
        ft, lt, rt = (i.lower() for i in (ftype, ltype, rtype))
        return f"accept_{ft}({lt[0]} {op} {rt[0]})"

    for i in (imports, *(_accept(t) for t in TYPES)):
        print(i)
        print()

    for t in TYPES:
        print(var(t))

    print("\n# Test unary ops")
    for ftype in TYPES:
        print(f"\n# {ftype=}")
        for rtype in TYPES:
            print()
            print(f"\n# {rtype=}")
            for op in UNARY.values():
                print(unary(ftype, op, rtype))

    print("\n# Test binary ops")

    for ftype in TYPES:
        print(f"\n# {ftype=}")
        for ltype in TYPES:
            print(f"\n# {ltype=}")
            for rtype in TYPES:
                print(f"\n# {rtype=}")
                for op in BINARY.values():
                    print(_binary(ftype, ltype, op, rtype))


def _accept(type: str) -> str:
    return f"""
def accept_{type}(x: {type}) -> Nonw:
    pass
"""


LOGICAL = {
    "eq": "==",
    "ne": "!=",
    "lt": "<",
    "gt": ">",
    "le": "<=",
    "ge": ">=",
}
UNARY = {
    "pos": "+",
    "neg": "-",
    "abs": "abs",
    "invert": "~",
    "round": "round",
    "floor": "math.floor",
    "ceil": "math.ceil",
    "trunc": "math.trunc",
}
BINARY = {
    "add": "+",
    "sub": "-",
    "mul": "*",
    "floordiv": "//",
    "div": "/",
    "mod": "%",
    # "divmod": "divmod",
    "pow": "**",
    "lshift": "<<",
    "rshift": ">>",
    "and": "&",
    "or": "|",
    "xor": "^",
}

OPS = *LOGICAL.values(), *BINARY.values(), *(f"{op}=" for op in BINARY.values())



TYPES = {
    'bool': "True",
    'int': "23",
    'Tensor': 'torch.randn(3, 3)',
    'float': "3.25",
    'str': "'xyzzy'",
}

IMPORTS = """\
import math

import torch
from torch import Tensor
""".strip()


if __name__ == "__main__":
    write_file()
