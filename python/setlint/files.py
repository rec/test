from pathlib import Path
from typing import Generator, List, Sequence, Set


def python_files(
    include: List[str], exclude: List[str], root: str='.'
) -> Generator[str, None, None]:
    include = [j for i in include for j in i.split(':')]
    exclude = [j for i in exclude for j in i.split(':')]

    iglobs = python_glob(Path(root), include, check_errors=True)
    eglobs = python_glob(Path(root), exclude, check_errors=False)

    return sorted(iglobs - eglobs)


def python_glob(root: Path, strings: Sequence[str], *, check_errors) -> Set[str]:
    result: Set[str] = set()

    nonexistent: List[str] = []
    not_python: List[str] = []

    for s in strings:
        p = root / s
        if p.is_dir():
            result.update(p.glob('**/*.py'))
        elif p.suffix != '.py':
            nonexistent.append(p)
        elif p.exists():
            result.add(p)
        else:
            not_python.append(p)

    if check_errors and (nonexistent or not_python):
        raise ValueError('\n'.join([
            (nonexistent and f'Nonexistent: {" ".join(nonexistent)}') or '',
            (not_python and f'Not Python: {" ".join(not_python)}') or '',
        ]))

    return result
