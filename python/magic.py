from itertools import product


def write_file():
    print(IMPORTS)
    for t in TYPES:
        print(f"def accept_{t.lower()}(x: {t}) -> None:\n    pass\n")

    if False:
        for t in TYPES:
            print(f"{t[0].lower()}: {t} = {TYPES[t]}")

    types = [t.lower() for t in TYPES]

    print("\n#\n# Test unary ops\n#")
    for atype in types:
        for op in UNARY:
            if len(op) == 1:
                print(f"accept_{atype}({op}{TENSOR})")
            else:
                print(f"accept_{atype}({op}({TENSOR}))")

    print("\n#\n# Test binary ops\n#")
    for atype in types:
        for type, v in TYPES.items():
            for op in BINARY_OPS:
                print(f"accept_{atype}({TENSOR} {op} {v})")

            if TENSOR != v:
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
    'int': "2",
    'Tensor': "randn(3)",
    'float': "1.5",
    'str': "'s'",
}
TENSOR = TYPES["Tensor"]

IMPORTS = """\
import math

from torch import randn, Tensor


"""


if __name__ == "__main__":
    write_file()
