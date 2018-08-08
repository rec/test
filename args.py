import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--foo', nargs='?', default='xxx')
print(parser.parse_args([]))
print(parser.parse_args(['--foo']))
