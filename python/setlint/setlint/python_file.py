import token
from tokenize import tokenize, TokenInfo
from .token_line import TokenLine
from .omitted_lines import OmittedLines

"""
Python's tokenizer splits Python code into lexical tokens tagged with one of many
token names. We are only interested in a few of these: references to the built-in `set`
will have to be in a NAME token, and we're only care about enough context to see if it's a
really `set` or, say, a method `set`.
"""


class PythonFile:
    filename: str
    lines: list[str]
    tokens: list[TokenInfo]
    token_lines: list[TokenLine]
    set_tokens: list[TokenInfo]

    def __init__(self, filename: str) -> None:
        self.filename = filename
        with open(filename) as fp:
            self.lines = fp.readlines()

        with open(filename, "rb") as fp:
            self.tokens = list(tokenize(fp.readline))

        self.token_lines = [TokenLine()]
        for t in self.tokens:
            self.token_lines[-1].append(t)
            if t.type == token.NEWLINE:
                self.token_lines.append(TokenLine())

        omitted = OmittedLines(filename)
        lines = [tl for tl in self.token_lines if not omitted(tl)]
        self.set_tokens = [t for tl in lines for t in tl.matching_tokens()]
