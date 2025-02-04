from itertools import product


def write_file():
    print(IMPORTS)
    print()
    print()

    for t in TYPES:
        print(f"def accept_{t.lower()}(x: {t}) -> None:\n    pass\n")

    for t in TYPES:
        print(f"{t[0].lower()}: {t} = {TYPES[t]}")

    types = [t.lower() for t in TYPES]

    print("\n#\n# Test unary ops\n#")
    for ftype in types:
        print(f"\n# {ftype=}")
        for rtype in types:
            print(f"\n# {rtype=}")
            for op in UNARY:
                if len(op) == 1:
                    print(f"accept_{ftype}({op}{rtype[0]})")
                else:
                    print(f"accept_{ftype}({op}({rtype[0]}))")

    print("\n#\n# Test binary ops\n#")
    for ftype in types:
        print(f"\n# {ftype=}")
        for ltype in types:
            print(f"\n# {ltype=}")
            for rtype in types:
                print(f"\n# {rtype=}")
                for op in BINARY_OPS:
                    print(f"accept_{ftype}({ltype[0]} {op} {rtype[0]})")


LOGICAL = {
    "eq": "==",
    "ne": "!=",
    "lt": "<",
    "gt": ">",
    "le": "<=",
    "ge": ">=",
}.values()

UNARY = {
    "pos": "+",
    "neg": "-",
    "abs": "abs",
    "invert": "~",
    "round": "round",
    "floor": "math.floor",
    "ceil": "math.ceil",
    "trunc": "math.trunc",
}.values()

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
}.values()

BINARY_OPS = *LOGICAL, *BINARY, *(f"{op}=" for op in BINARY)


TYPES = {
    'bool': "True",
    'int': "23",
    'Tensor': 'torch.randn(3, 3)',
    'float': "3.25",
    'str': "'xyzzy'",
}

IMPORTS = """
import math

import torch
from torch import Tensor
""".strip()


if __name__ == "__main__":
    write_file()
