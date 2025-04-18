import itertools
import json
import sys
import token
from pathlib import Path
from tokenize import generate_tokens, TokenInfo
from typing import Iterator

FILTER_BELOW = 5


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
    words = line.split()
    loc = words.index("import")
    before = " ".join(words[0:loc])
    after = " ".join(words[loc + 1:])
    assert after, line
    after = after.replace("(", "").replace(")", "").strip()
    parts = [ps.split()[0] for p in after.split(",") if (ps := p.strip())]

    if before:
        before, _, imp = before.strip().partition("from ")
        assert not before, f"{before=}, {line[:120]=}"
        parts = [f"{imp}.{p}" for p in parts]

    return parts


def all_python_files(path: str, prefix="", python_root=None):
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

    it = bucket((mp, i) for f in paths for mp, i in one_file(f)).items()
    file_to_imports = {k: sorted(i for i in v if i.startswith(prefix)) for k, v in it}

    imports = {}
    for file, imps in file_to_imports.items():
        for i in imps:
            if i in file_to_imports:
                module, symbol = i, "(module)"
            else:
                module, _, symbol = i.rpartition(".")
            imports.setdefault(module, {}).setdefault(symbol, []).append(file)

    for i in imports.values():
        for k, v in i.items():
            v.sort()

    items = imports.items()
    sum1 = {k: {j: len(w) for j, w in v.items()} for k, v in items}
    sum2 = {k: sum(i for i in v.values()) for k, v in sum1.items()}

    def sort_by_value(d):
        return dict(sorted(d.items(), key=lambda kv: kv[1], reverse=True))

    sum1 = {k: sort_by_value(v) for k, v in sum1.items()}
    sum2 = sort_by_value(sum2)
    sum1 = {k: sum1[k] for k in sum2}

    def is_big(x):
        try:
            return len(x) >= FILTER_BELOW
        except TypeError:
            return x >= FILTER_BELOW

    def only_big(d):
        if isinstance(d, dict):
            return {k: v for k, v in d.items() if is_big(v)}
        if isinstance(d, list):
            return [k for k in d if is_big(k)]
        assert False

    def only_bigd(d):
        return {k: s for k, v in d.items() if (s := only_big(v))}

    def non_empty(d):
        return {k: v for k, v in d.items() if v}

    sum2 = only_big(sum2)
    sum1 = {k: sum1[k] for k in sum2}
    sum1 = only_bigd(sum1)

    imports = {k: imports[k] for k in sum2}
    imports = {k: only_bigd(v) for k, v in imports.items()}

    result = [sum2, sum1, imports]
    for r in result:
        print(json.dumps(r, indent=2, sort_keys=False))



def one_file(f):
    module_path = [i.name for i in reversed(f.parents) if i.name]
    if any('.' in i for i in module_path):
        return
    mp = ".".join(module_path + (f.stem != "__init__") * [f.stem])

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
