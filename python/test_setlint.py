import setlint
import token

EXPECTED_TOKENS = [
    [('NAME', 'a'), ('OP', '='), ('NAME', 'set'), ('OP', '('), ('OP', ')')],
    [('NAME', 'b'), ('OP', '='), ('STRING', "'set()'")],
    [('NAME', 'c'), ('OP', '='), ('NAME', 'set')],
    [('NAME', 'd'), ('OP', '='), ('NAME', 'c'), ('OP', '.'), ('NAME', 'set')],
    [('NAME', 'f'), ('OP', '='), ('OP', '('), ('NAME', 'set'), ('OP', '('), ('OP', ')'), ('OP', ')')],
    [('NAME', 'e'), ('OP', '='), ('STRING', '""" set()\nset() set x.set set()\n\\""""')],
]

EXPECTED_SETS = [
[
    (
        'setlint-sample.txt',
        "TokenInfo(type=1 (NAME), string='set', start=(1, 4), end=(1, 7), "
        "line='a = set()\\n')",
    ),
    (
        'setlint-sample.txt',
        "TokenInfo(type=1 (NAME), string='set', start=(3, 4), end=(3, 7), "
        "line='c = set\\n')",
    ),
    (
        'setlint-sample.txt',
        "TokenInfo(type=1 (NAME), string='set', start=(6, 3), end=(6, 6), "
        "line='   set(\\n')",
    ),
]


def test_get_tokens():
    def _pair(t):
        return token.tok_name[t.type], t.string


    tokens = setlint.get_tokens('setlint-sample.txt')
    actual = [[_pair(t) for t in tl] for tl in tokens]
    assert actual == EXPECTED_TOKENS


def test_all_sets():
    all_sets = list(setlint.all_sets(['setlint-sample.txt']))
    actual = [(s, str(t)) for s, t in all_sets]
    assert actual == EXPECTED_SETS