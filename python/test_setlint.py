import tokenize as tok

with open('setlint-sample.txt', 'rb') as fp:
    for t in tok.tokenize(fp.readline):
        name = tok.tok_name[t.type]
        if t.type in (tok.NAME, tok.STRING, tok.OP):
            print(name, t.string)
        elif t.type in (tok.NEWLINE, tok.NL):
            print('   ', name)
