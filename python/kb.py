import json
import argparse
from pathlib import Path

def replacer(value: dict, depth: int=100000000) -> dict:
    if depth == 0:
        return value

    modified = value.copy()

    for key in modified.keys():
        if type(modified[key]) is dict:
            modified[key] = replacer(modified[key], depth - 1)
        else:
            modified[key] = {
                '_content': modified[key],
                '_type': str(type(modified[key]))
            }

    return modified

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('input')
    parser.add_argument('depth')
    parser.add_argument('output')

    args = parser.parse_args()

    inputPath = Path(args.input)
    outputPath = Path(args.output)

    if not inputPath.exists():
        print(inputPath, 'does not exist')
        raise SystemExit(1)

    try:
        depth = int(args.depth)
    except ValueError:
        print('Please input depth as integer')
        raise SystemExit(1)


    inputFile = open(inputPath, 'r', encoding='utf-8')
    inputStr = inputFile.read()
    inputFile.close()

    outputFile = open(outputPath, 'w', encoding='utf-8')

    outputStr = json.dump(replacer(json.loads(inputStr), depth), outputFile, indent=4)
    outputFile.close()
