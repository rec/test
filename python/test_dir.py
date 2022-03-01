from pathlib import Path
import tdir

FILE = Path('file.txt')

for i in range(50):
    with tdir():
        print(Path().absolute())
        assert not list(Path().iterdir())
        FILE.write_text('hello')
        assert list(Path().iterdir())
