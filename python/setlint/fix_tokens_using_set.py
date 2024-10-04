from tokens_using_set import TokensUsingSet
from typing import List


def fix_tokens_using_set(tokens: TokensUsingSet) -> int:
    if not tokens.tokens:
        return 0

    # First replace all the instances of set with OrderedSet
    with open(tokens.filename) as fp:
        lines = fp.readlines()

    reverse_tokens = sorted(tokens.tokens, key=lambda t: t.start, reverse=True)
    for count, t in enumerate(reverse_tokens):
        (start_line, start_col), (end_line, end_col) = t.start, t.end
        assert start_line == end_line
        line = lines[start_line]

        a, b, c = line[:start_col], line[start_col:end_col], line[end_col:]
        assert b == 'set'
        lines[start_line] = f'{a}OrderedSet{c}'

    if not any(_match_import(line) for line in lines):
        # Add the missing import and hope that ruff puts it in the right place
        _add_import(lines, tokens)
        count += 1

    with open(tokens.filename, 'w') as fp:
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


def _add_import(lines: List[str], tokens: TokensUsingSet):
    pass
