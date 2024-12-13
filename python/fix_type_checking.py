from pathlib import Path
import re

line_re = re.compile(r'[a-z_0-9/]+\.py:\d+:')


def get_lines():
    with p.open() as fp:
        return [i.rstrip() for i in fp]


def segment_lines(lines: list[str]):
    segments = {}
    segment = []
    for line in lines:
        if line_re.match(line):
            assert line not in segments
            segment = []
            segments[line] = segment
        else:
            segment.append(line)
    return segments


def is_type_checking(lines: list[str]):
    return any('WARNING (RUFF) TCH' in lines)


def combine_segments(segments):
    result = {}
    for filename, segment in segments.items():
        name, lineno, nothing = filename.split(':')
        assert not nothing
        result.setdefault(name, []).append(int(lineno))

    return result
