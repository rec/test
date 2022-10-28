import subprocess
from pathlib import Path

ROOT = Path('/Users/tom/Downloads/videos/Northern Exposure')
SRC = ROOT / 'original'
TARGET = ROOT / 'processed'


def main(src=SRC, target=TARGET):
    for s in sorted(s for s in src.iterdir() if s.is_dir()):
        for f in sorted(t for t in s.iterdir() if t.suffix == '.mkv'):
            tf = target / f.relative_to(src).with_suffix('.mp4')
            if tf.exists():
                continue

            tf.parent.mkdir(parents=True, exist_ok=True)
            cmd = (
                'ffmpeg',
                '-i', str(f),
                '-c:v', 'h264_videotoolbox',
                '-b:v', '3600k',
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
    main()
