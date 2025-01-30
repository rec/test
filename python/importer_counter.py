import itertools
import json
import sys
import token
from pathlib import Path
from tokenize import generate_tokens, TokenInfo
from typing import Iterator


def import_lines(tokens) -> Iterator[str]:
    it = (t for t in tokens if t.type not in (token.COMMENT, token.NL))
    for _, i in itertools.groupby(it, lambda t: t.type == token.NEWLINE):
        token_list = list(i)
        t = token_list and token_list[0]
        if t and t.type == token.NAME and t.string in ("from", "import"):
            lines = {j.start[0]: j.line for j in token_list}
            yield " ".join(" ".join(lines.values()).split()).strip()


def split_import(line):
    if "*" in line:
        return []

    before, _, after = line.partition('import')
    assert after, line
    after = after.replace("(", "").replace(")", "").strip()
    parts = [ps.split()[0] for p in after.split(",") if (ps := p.strip())]

    if before:
        before, _, imp = before.strip().partition("from ")
        assert not before, f"{before=}, {line[:120]=}"
        parts = [f"{imp}.{p}" for p in parts]

    return parts


def all_python_files(path: str, prefix=None, python_root=None):
    result = {}
    python_root = python_root or Path(".")
    path = Path(path)
    path = path.relative_to(python_root)
    if path.suffix == ".py":
        paths = [path]
    else:
        paths = sorted(path.glob("**/*.py"))

    def bucket(it):
        result = {}
        for k, v in it:
            result.setdefault(k, []).append(v)
        return result

    result = bucket((mp, i) for f in paths for mp, i in one_file(f))
    if prefix:
        result = {k: [i for i in v if i.startswith(prefix)] for k, v in result.items()}
    inverse = bucket((i, k) for k, v in result.items() for i in v)
    print(json.dumps([result, inverse], indent=2, sort_keys=True))


def one_file(f):
    module_path = [i.name for i in reversed(f.parents) if i.name]
    if any('.' in i for i in module_path):
        return
    mp = ".".join(module_path + [f.stem])

    with f.open() as fp:
        tokens = list(generate_tokens(fp.readline))

    for line in import_lines(tokens):
        for imp in split_import(line):
            simp = imp.lstrip(".")
            if diff := len(imp) - len(simp):
                imp = ".".join(module_path[:(1 - diff) or None] + [simp])
            yield mp, imp


if __name__ == '__main__':
     all_python_files(*sys.argv[1:])
