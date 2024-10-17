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


class TokenLines:
    filename: str
    lines: list[TokenLine]
    tokens: list[TokenInfo]

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.lines = [TokenLine()]

        with open(filename, "rb") as fp:
            for t in tokenize(fp.readline):
                self.lines[-1].append(t)
                if t.type == token.NEWLINE:
                    self.lines.append(TokenLine())

        omitted = OmittedLines(filename)
        self.tokens = []

        for line in self.lines:
            if not omitted(line.lines_covered()):
                self.tokens.extend(line.tokens_using_set())
