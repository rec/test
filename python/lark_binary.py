import lark

GRAMMAR = r"""
start: "f" /oo.*ba/ "r"
"""

p = lark.Lark(GRAMMAR, parser='lalr', lexer='standard',         propagate_positions=False,
        maybe_placeholders=False,
)
print(p.parse('foo bar'))

p = lark.Lark(GRAMMAR, parser='lalr', lexer='standard', use_bytes=True,        propagate_positions=False,
        maybe_placeholders=False,
)

pp = p.parse(b'foo bar')
print(pp)
