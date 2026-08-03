    OPEN, CLOSE = '([{<', ')]}>'


    def is_matching(s: str) -> bool:
        stack = []
        for c in s:
            if c in OPEN:
                stack.append(c)
            elif c in CLOSE:
                if not stack:
                    return False
                b = stack.pop()
                if not (
                    (b == '(' and c == ')')
                    or (b == '[' and c == ']')
                    or (b == '{' and c == '}')
                    or (b == '<' and c == '>')
                ):
                    return False
        return True
