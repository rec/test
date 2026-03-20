from __future__ import annotations

import dataclasses as dc
from collections.abc import Iterable
from tokenize import TokenInfo, Untokenizer, generate_tokens

import token
import itertools

_IGNORED_TYPES = {token.COMMENT, token.ENCODING}


def rewrite_multi_lambdas(filename: str):
    with open(filename) as fp:
        tokens = list(generate_tokens(fp.readline))

    newlines = [-1, *(i for i, t in enumerate(tokens) if t.type == token.NEWLINE)]
    lines = list(itertools.pairwise([-1] + newlines))
    it = enumerate(tokens)
    double_colons = [i for i, t in it if i and t.string == tokens[i - 1].string == ':']

    closing_colons = []
    for i in range(0, len(double_colons), 2):
        # Find end of parameter list
        begin, end = double_colons[i:i + 2]
        depth = 0
        for close in range(begin + 1, end):
            t = tokens[close]
            depth += (t.string in ('{', '(', '[')) - (t.string in ('}', ')', ']'))
            if not depth:
                break

        for close in range(close + 1, end):
            if (t := tokens[close]).string == ':'):
                closing_colons.append(close)
                break

    with open(filename) as fp:
        lines = list(fp)
