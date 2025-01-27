from pathlib import Path
import re

ident = "([._A-Za-z0-9]+)"
importer = f"(?:import {ident})|(?:from {ident} import {ident})"
match_import = re.compile(importer).match


def list_imports(path: Path):
    for f in path.glob("**/*.py"):
        r = f.relative_to(path)
        module_path = [i.name for i in reversed(r.parents) if i != path] + [r.stem]
        if any('.' in i for i in module_path):
            continue
        mp = '.'.join(module_path)

        with f.open() as fp:
            for line in fp:
                if m := match_import(line.partition("#")[0].strip()):
                    a, b, c = m.groups()
                    if a is None:
                        assert b is not None and c is not None
                        name = f"{b}.{c}"
                        arg = module_path, b, c
                    else:
                        assert b is None and c is None
                        name = a
                        arg = module_path, a
                    yield arg


def main(path="."):
    for i in list_imports(Path(path)):
        print(i)


if __name__ == '__main__':
    main()
