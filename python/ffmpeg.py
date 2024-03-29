import subprocess as sp
from pathlib import Path
import re

KBS_RE = re.compile(r'bitrate: \s+ (\d+) \s+ kb/s', re.VERBOSE)
BOOST_RATIO = 1.1


def main(src, target):
    src, target = Path(src), Path(target)
    assert src.exists(), str(src)
    if src.suffix in ('.avi', '.mkv', '.mp4'):
        files = [src]
        src = src.parent
    else:
        files = sorted((*src.glob('**/*.mkv'), *src.glob('**/*.mp4')))

    for f in files:
        tf = target / f.relative_to(src).with_suffix('.mp4')
        if tf.exists():
            tf.unlink()

        cmd = 'ffmpeg', '-i', str(f)
        out = sp.run(cmd, text=True, stderr=sp.PIPE).stderr
        out = ' '.join(out.splitlines())
        m = KBS_RE.findall(out)

        bvs = [int(BOOST_RATIO * int(i)) for i in m]
        bv = sum(bvs)
        print()
        print(*bvs, f)
        print()
        if not True:
            # print('$', *cmd)
            continue

        cmd += (
            '-acodec', 'aac',
            '-c:v', 'h264_videotoolbox',
            '-b:v', f'{bv}k',
            str(tf)
        )
        tf.parent.mkdir(parents=True, exist_ok=True)
        try:
            finished = False
            sp.run(cmd)
            finished = True
        finally:
            if not finished:
                tf.unlink()


if __name__ == '__main__':
    import sys

    *src, target = sys.argv[1:]

    for s in src:
        main(s, target)
