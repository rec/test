from is_token_using_set import TokenLine
from tokenize import TokenInfo
from typing import Sequence


def fix_tokens_using_set(
    filename: str,
    tokens: Sequence[TokenInfo],
    token_lines: Sequence[TokenLine],
) -> int:
    if not tokens:
        return 0

    # First replace all the instances of set with OrderedSet
    with open(filename) as fp:
        lines = fp.readlines()

    for count, t in enumerate(tokens.sorted(key=lambda t: t.first, reverse=True)):
        start_line, start_col = t.start
        end_line, end_col = t.end
        assert start_line == end_line
        line = lines[start_line]
        assert line[start_col:end_col] == 'set'
        pre, post = line[:start_col], line[end_col:]

        lines[start_line] = f'{pre}OrderedSet{post}'

    if not any(_match_import(line) for line in lines):
        # Add the missing import and hope that ruff puts it in the right place
        _add_import(lines)
        count += 1

    with open(filename, 'w') as fp:
        fp.writelines(lines)

    return count


def _match_import(line: str) -> bool:
    p = [j for i in line.split() for j in i.split('.') if j]
    return (
        bool(p)
        and p[0] == 'from'
        and p[-1] == 'OrderedSet'
        and 'import' in p and 'utils' in p
    )


def _add_import(lines):
    pass
