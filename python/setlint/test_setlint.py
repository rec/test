from setlint.python_file import PythonFile
from setlint.omitted_lines import OmittedLines
import token
from tokenize import TokenInfo

TESTFILE = "testdata/sample.py.txt"
TESTFILE_OMITTED = "testdata/sample-omitted.py.txt"


def test_get_all_tokens():
    assert EXPECTED_SETS == PythonFile(TESTFILE).set_tokens


def test_omitted_lines():
    actual = sorted(OmittedLines(TESTFILE_OMITTED).lines)
    expected = [1, 5, 12]
    assert expected == actual


def test_all_sets_omitted():
    assert EXPECTED_SETS_OMITTED == PythonFile(TESTFILE_OMITTED).set_tokens


def _token_info(start, end, line):
    return TokenInfo(type=token.NAME, string="set", start=start, end=end, line=line)


EXPECTED_SETS = [
    _token_info((1, 4), (1, 7), "a = set()\n"),
    _token_info((3, 4), (3, 7), "c = set\n"),
    _token_info((6, 3), (6, 6), "   set(\n"),
]

EXPECTED_SETS_OMITTED = [
    _token_info((2, 4), (2, 7), "a = set()\n"),
    _token_info((4, 4), (4, 7), "c = set\n"),
    _token_info((8, 3), (8, 6), "   set(\n"),
]
