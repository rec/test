from pathlib import Path
from setlint.python_file import OmittedLines, PythonFile
from setlint import fix_set_tokens
import token
from tokenize import TokenInfo
import pytest

TESTFILE = "testdata/sample.py.txt"
TESTFILE_OMITTED = "testdata/sample-omitted.py.txt"
INCLUDES_FILE = "testdata/includes.py.txt"
INCLUDES_FILE2 = "testdata/includes2.py.txt"


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


def _fix_set_tokens(filename):
    actual, count = fix_set_tokens.fix_set_tokens(PythonFile(filename))
    expected_file = Path(filename + ".expected")
    if expected_file.exists():
        with expected_file.open() as fp:
            expected = fp.readlines()
    else:
        expected_file.write_text("".join(actual))
        expected = actual

    return count, actual, expected


@pytest.mark.parametrize(
    "filename, count",
    (
        (TESTFILE, 4),
        (TESTFILE_OMITTED, 4),
        (INCLUDES_FILE, 1),
        (INCLUDES_FILE2, 2),
    ),
)
def test_fix_set_token(filename, count):
    actual_count, actual, expected = _fix_set_tokens(filename)
    assert actual == expected
    assert actual_count == count


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
