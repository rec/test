from find_set_tokens import FindSetTokens
import token

TESTFILE = FindSetTokens('setlint-sample.txt')
TESTFILE2 = FindSetTokens('setlint-sample-2.txt')

EXPECTED_TOKENS = [
    [('NAME', 'a'), ('OP', '='), ('NAME', 'set'), ('OP', '('), ('OP', ')')],
    [('NAME', 'b'), ('OP', '='), ('STRING', "'set()'")],
    [('NAME', 'c'), ('OP', '='), ('NAME', 'set')],
    [('NAME', 'd'), ('OP', '='), ('NAME', 'c'), ('OP', '.'), ('NAME', 'set')],
    [('NAME', 'f'), ('OP', '='), ('OP', '('), ('NAME', 'set'), ('OP', '('), ('OP', ')'), ('OP', ')')],
    [('NAME', 'e'), ('OP', '='), ('STRING', '""" set()\nset() set x.set set()\n\\""""')],
]

EXPECTED_SETS = [
    (
        "TokenInfo(type=1 (NAME), string='set', start=(1, 4), end=(1, 7), "
        "line='a = set()\\n')"
    ),
    (
        "TokenInfo(type=1 (NAME), string='set', start=(3, 4), end=(3, 7), "
        "line='c = set\\n')"
    ),
    (
        "TokenInfo(type=1 (NAME), string='set', start=(6, 3), end=(6, 6), "
        "line='   set(\\n')"
    ),
]


EXPECTED_SETS2 = [
    (
        "TokenInfo(type=1 (NAME), string='set', start=(2, 4), end=(2, 7), "
        "line='a = set()\\n')"
    ),
    (
        "TokenInfo(type=1 (NAME), string='set', start=(4, 4), end=(4, 7), "
        "line='c = set\\n')"
    ),
    (
        "TokenInfo(type=1 (NAME), string='set', start=(8, 3), end=(8, 6), "
        "line='   set(\\n')"
    ),
]


def test_get_all_tokens():
    def _pair(t):
        return token.tok_name[t.type], t.string

    tokens = TESTFILE._token_lines()
    actual = [[_pair(t) for t in tl] for tl in tokens]
    assert actual == EXPECTED_TOKENS


def test_find_set_tokens():
    actual = [str(i) for i in TESTFILE.set_tokens]
    assert len(actual) == len(EXPECTED_SETS)
    assert actual == EXPECTED_SETS


def test_omitted_lines():
    actual = sorted(TESTFILE2._omitted_lines)
    expected = [1, 5, 12]
    assert actual == expected


def test_all_sets_omitted():
    actual = [str(i) for i in TESTFILE2.set_tokens]
    assert len(actual) == len(EXPECTED_SETS2)
    assert actual == EXPECTED_SETS2
