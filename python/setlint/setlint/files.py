from pathlib import Path
from typing import Sequence


def resolve_python_files(
    include: list[str], exclude: list[str], root: str = "."
) -> list[Path]:
    include = [j for i in include for j in i.split(":")]
    exclude = [j for i in exclude or () for j in i.split(":")]

    iglobs = python_glob(Path(root), include, check_errors=True)
    eglobs = python_glob(Path(root), exclude, check_errors=False)

    return sorted(iglobs - eglobs)


def python_glob(root: Path, strings: Sequence[str], *, check_errors) -> set[Path]:
    result: set[Path] = set()

    nonexistent: list[str] = []
    not_python: list[str] = []

    for s in strings:
        p = root / s
        if p.is_dir():
            result.update(p.glob("**/*.py"))
        elif p.suffix != ".py":
            nonexistent.append((str(p)))
        elif p.exists():
            result.add(p)
        else:
            not_python.append(str(p))

    if check_errors and (nonexistent or not_python):
        raise ValueError(
            "\n".join(
                [
                    (nonexistent and f'Nonexistent: {" ".join(nonexistent)}') or "",
                    (not_python and f'Not Python: {" ".join(not_python)}') or "",
                ]
            )
        )

    return result
