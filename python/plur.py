from numbers import Number
from typing import Sequence, Union

Arg = Union[Number, Sequence, str]

DEFAULT_PLURAL = 's'


def plur(word: str, plural: str, *args: Tuple[Arg, ...], zero=None) -> str:
    if not args or isinstance(args[-1], str):
        return partial(plur, word, plural, *args, zero=zero)

    *plurals, count = plural, *args
    try:
        n = len(count)
    except TypeError:
        n = count

    if n == 0:
        p = plurals[-1] if zero is None else zero
    elif n == 1:
        p = word
    else:
        p = plurals[min(n, len(plurals) - 1)]

     word + p[1:] if p.startswith('-') else p
