from setlint.token_lines import TokenLines
from setlint.omitted_lines import OmittedLines
import token
from tokenize import TokenInfo

TESTFILE = "testdata/setlint-sample.txt"
TESTFILE_OMITTED = "testdata/setlint-sample-omitted.txt"


def test_get_all_tokens():
    assert EXPECTED_SETS == TokenLines(TESTFILE).tokens


def test_omitted_lines():
    actual = sorted(OmittedLines(TESTFILE_OMITTED).lines)
    expected = [1, 5, 12]
    assert expected == actual


def test_all_sets_omitted():
    assert EXPECTED_SETS_OMITTED == TokenLines(TESTFILE_OMITTED).tokens


EXPECTED_SETS = [
    TokenInfo(
        type=token.NAME, string="set", start=(1, 4), end=(1, 7), line="a = set()\n"
    ),
    TokenInfo(
        type=token.NAME, string="set", start=(3, 4), end=(3, 7), line="c = set\n"
    ),
    TokenInfo(
        type=token.NAME, string="set", start=(6, 3), end=(6, 6), line="   set(\n"
    ),
]

EXPECTED_SETS_OMITTED = [
    TokenInfo(
        type=token.NAME, string="set", start=(2, 4), end=(2, 7), line="a = set()\n"
    ),
    TokenInfo(
        type=token.NAME, string="set", start=(4, 4), end=(4, 7), line="c = set\n"
    ),
    TokenInfo(
        type=token.NAME, string="set", start=(8, 3), end=(8, 6), line="   set(\n"
    ),
]
