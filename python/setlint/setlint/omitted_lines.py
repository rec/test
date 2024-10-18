from .token_line import TokenLine

OMIT_COMMENT = "# noqa: setlint"


class OmittedLines:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.lines = set()
        with open(self.filename) as fp:
            for i, s in enumerate(fp):
                if s.rstrip().endswith(OMIT_COMMENT):
                    self.lines.add(i + 1)  # Tokenizer lines start at 1

    def __call__(self, tl: TokenLine) -> bool:
        # A TokenLine might span multiple physical lines
        return bool(self.lines.intersection(tl.lines_covered()))
