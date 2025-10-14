import tokenize
import sys

with open(sys.argv[1]) as fp:
    for token in tokenize.generate_tokens(fp.readline):
        print(token)
