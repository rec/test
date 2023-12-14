from pathlib import Path
import json
import safer
import tdir

FILENAME = Path('one')
FAIL = True


@tdir
def test_wrapper_bug():
    if FAIL:
        fp = open(FILENAME, 'w')
        with safer.writer(fp, close_on_exit=True) as writer:
            writer.write('hello, world')
        assert FILENAME.read_text() == 'hello, world'
    else:
        with safer.writer(FILENAME, close_on_exit=True) as writer:
            writer.write('hello, world')
        assert FILENAME.read_text() == 'hello, world'
        assert False


if __name__ == '__main__':
    test_wrapper_bug()
