import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--foo', nargs='?', default='xxx')
parser.add_argument('-3', action='store_true')
print(parser.parse_args([]))
print(parser.parse_args(['--foo']))
print(parser.parse_args(['-3']))

print(parser.parse_args([]).f)
