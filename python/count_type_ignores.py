from pathlib import Path
import json, token, tokenize


def all_python_files(path: str, python_root=None):
    python_root = python_root or Path(".")
    path = Path(path).relative_to(python_root)
    if path.suffix == ".py":
        paths = [path]
    else:
        paths = path.glob("**/*.py")

    ignores = {str(p): count for p in paths if (count := count_file(p))}
    ignores = dict(sorted(ignores.items(), key=lambda x: x[1], reverse=True))
    print(json.dumps(ignores, indent=2))


def count_file(p: Path) -> int:
    with p.open() as fp:
        return sum(is_ignore(t) for t in tokenize.generate_tokens(fp.readline))


def is_ignore(t: tokenize.Token) -> bool:
     return t.type == token.COMMENT and "type: ignore[" in t.string


if __name__ == "__main__":
     import sys

     all_python_files(*sys.argv[1:])
