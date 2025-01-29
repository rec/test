from pathlib import Path
import itertools
import re

ident = "([._A-Za-z0-9]+)"
importer = f"(?:import {ident})|(?:from {ident} import {ident})"
match_import = re.compile(importer).match


def list_imports(path: Path, python_root=None):
    results = {}
    python_root = python_root or Path(".")
    print(path.absolute(), python_root.absolute())
    for f in path.glob("**/*.py"):
        r = f.relative_to(python_root)
        module_path = [i.name for i in reversed(r.parents)][1:]
        if any('.' in i for i in module_path):
            continue
        mp = '.'.join(module_path)

        with f.open() as fp:
            for line in fp:
                if m := match_import(line.partition("#")[0].strip()):
                    print(f"{f}:", line.rstrip())
                    a, b, c = m.groups()
                    if a is None:
                        assert b is not None and c is not None
                        bs = b.rstrip(".")
                        if diff := len(b) - len(bs):
                            s = module_path[:(1 - diff) or None]
                        else:
                            s = []
                        name = ".".join(s + [c])
                    else:
                        assert b is None and c is None
                        name = a
                    results.setdefault(name, []).append(str(r))

    return {k: sorted(v) for k, v in sorted(results.items())}


def main(parts):
    results = list_imports(*(Path(p) for p in parts))
    results = ((k, len(v)) for k, v in results.items() if k.startswith('torch.'))
    results = dict(sorted(results, key=lambda r: r[1]))

    if False:
        import json
        print(json.dumps(results, indent=2))


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
