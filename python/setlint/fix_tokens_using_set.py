from token_line import TokenLine
from tokens_using_set import TokensUsingSet
from typing import Dict, List, Tuple
import token


def fix_tokens_using_set(tokens: TokensUsingSet) -> Tuple[List[str], int]:
    if not tokens.tokens:
        return [], 0

    # First replace all the instances of set with OrderedSet
    with open(tokens.filename) as fp:
        contents = fp.readlines()

    reverse_tokens = sorted(tokens.tokens, key=lambda t: t.start, reverse=True)
    for count, t in enumerate(reverse_tokens):
        (start_line, start_col), (end_line, end_col) = t.start, t.end
        assert start_line == end_line
        line = contents[start_line]

        a, b, c = line[:start_col], line[start_col:end_col], line[end_col:]
        assert b == "set"
        contents[start_line] = f"{a}OrderedSet{c}"

    if not any(_match_import(line) for line in contents):
        # Add the missing import and hope that ruff puts it in the right place
        _add_import(contents, tokens)
        count += 1

    return contents, count


def _match_import(line: str) -> bool:
    p = [j for i in line.split() for j in i.split(".") if j]
    return (
        bool(p)
        and p[0] == "from"
        and p[-1] == "OrderedSet"
        and "import" in p
        and "utils" in p
    )


def _add_import(contents: List[str], tokens: TokensUsingSet):
    lines: Dict[str, List[TokenLine]] = {}
    for tl in tokens.token_lines:
        t = tl.tokens[0]
        if t.type == token.NAME:
            lines.setdefault(t.string, []).append(tl)
    """


    lasts = {tl[0].string: tl for tl in lines[]

            lasts[tl[0].string] = tl




    froms = [tl for tl in tokens.token_lines if accept(tl, 'from')]
    """
