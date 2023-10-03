import subprocess
from pathlib import Path


def main(src, target, bv='4800k'):
    src, target = Path(src), Path(target)
    assert src.exists(), str(src)
    for f in sorted(t for t in src.iterdir() if t.suffix in ('.mkv', '.mp4')):
        tf = target / f.relative_to(src).with_suffix('.mp4')
        if False and tf.exists():
            continue

        tf.parent.mkdir(parents=True, exist_ok=True)
        cmd = (
            'ffmpeg',
            '-i', str(f),
            '-c:v', 'h264_videotoolbox',
            '-b:v', f'{bv}',
            str(tf)
        )
        print('$', *cmd)
        if not True:
            continue

        try:
            finished = False
            subprocess.run(cmd)
            finished = True
        finally:
            if not finished:
                tf.unlink()


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
