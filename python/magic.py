from itertools import product


def write_file():
    print(HEADER)

    for t in TYPES:
        print(f"def accept_{t.lower()}(x: {t}) -> None:\n    pass\n")

    types = [t.lower() for t in TYPES]
    atypes = ['tensor', 'str']

    print("\n#\n# Test unary ops\n#")
    for atype in types:
        print()
        for op in UNARY:
            if len(op) == 1:
                print(f"accept_{atype}({op}{TENSOR})")
            else:
                print(f"accept_{atype}({op}({TENSOR}))")

    print("\n#\n# Test binary ops\n#")
    for type, v in TYPES.items():
        if type == 'str':
            continue
        for atype in types:
            print()
            for op in BINARY_OPS:
                print(f"accept_{atype}({TENSOR} {op} {v})")

            if TENSOR != v and not op.endswith("="):
                print()
                for op in BINARY_OPS:
                    print(f"accept_{atype}({v} {op} {TENSOR})")


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
    "invert": "~",
    # "abs": "abs",
    # "round": "round",
    # "floor": "math.floor",
    # "ceil": "math.ceil",
    # "trunc": "math.trunc",
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

BINARY_OPS = *LOGICAL, *BINARY  # , *(f"{op}=" for op in BINARY)

TYPES = {
    'str': "'s'",
    'Tensor': "T",
    'bool': "True",
    'int': "2",
    'float': "1.5",
}
TENSOR = TYPES["Tensor"]

HEADER = """\
import math

from torch import randn, Tensor


T = randn(3)

"""


if __name__ == "__main__":
    write_file()
