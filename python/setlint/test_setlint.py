from setlint.tokens_using_set import TokensUsingSet
from setlint.omitted_lines import OmittedLines
import token
from tokenize import TokenInfo

TESTFILE = TokensUsingSet("testdata/setlint-sample.txt")
TESTFILE_OMITTED = TokensUsingSet("testdata/setlint-sample-omitted.txt")


def test_token_lines():
    def _pair(t):
        return token.tok_name[t.type], t.string

    actual = [[_pair(t) for t in tl.tokens] for tl in TESTFILE.token_lines]
    assert EXPECTED_LINES == actual


def test_get_all_tokens():
    assert EXPECTED_SETS == TESTFILE.tokens


def test_omitted_lines():
    actual = sorted(OmittedLines(TESTFILE_OMITTED.filename).lines)
    expected = [1, 5, 12]
    assert expected == actual


def test_all_sets_omitted():
    assert TESTFILE_OMITTED.tokens == EXPECTED_SETS_OMITTED


EXPECTED_SETS = [
    TokenInfo(type=token.NAME, string='set', start=(1, 4), end=(1, 7), line='a = set()\n'),
    TokenInfo(type=token.NAME, string='set', start=(3, 4), end=(3, 7), line='c = set\n'),
    TokenInfo(type=token.NAME, string='set', start=(6, 3), end=(6, 6), line='   set(\n'),
]

EXPECTED_SETS_OMITTED = [
    TokenInfo(type=token.NAME, string='set', start=(2, 4), end=(2, 7), line='a = set()\n'),
    TokenInfo(type=token.NAME, string='set', start=(4, 4), end=(4, 7), line='c = set\n'),
    TokenInfo(type=token.NAME, string='set', start=(8, 3), end=(8, 6), line='   set(\n'),
]

EXPECTED_LINES = [
    [("NAME", "a"), ("OP", "="), ("NAME", "set"), ("OP", "("), ("OP", ")")],
    [("NAME", "b"), ("OP", "="), ("STRING", "'set()'")],
    [("NAME", "c"), ("OP", "="), ("NAME", "set")],
    [("NAME", "d"), ("OP", "="), ("NAME", "c"), ("OP", "."), ("NAME", "set")],
    [
        ("NAME", "f"),
        ("OP", "="),
        ("OP", "("),
        ("NAME", "set"),
        ("OP", "("),
        ("OP", ")"),
        ("OP", ")"),
    ],
    [
        ("NAME", "e"),
        ("OP", "="),
        ("STRING", '""" set()\nset() set x.set set()\n\\""""'),
    ],
    [("NAME", "class"), ("NAME", "A"), ("OP", ":")],
    [
        ("NAME", "def"),
        ("NAME", "set"),
        ("OP", "("),
        ("NAME", "self"),
        ("OP", ","),
        ("NAME", "x"),
        ("OP", ")"),
        ("OP", ":"),
    ],
    [("NAME", "self"), ("OP", "."), ("NAME", "x"), ("OP", "="), ("NAME", "x")],
    [
        ("NAME", "set"),
        ("OP", "="),
        ("NAME", "A"),
        ("OP", "("),
        ("OP", ")"),
        ("OP", "."),
        ("NAME", "set"),
    ],
    [('NAME', 'good'), ('OP', '='), ('OP', '{'), ('OP', '}')],
    [('NAME', 'bad'), ('OP', '='), ('OP', '{'), ('OP', '}')],
]
