from pathlib import Path
import shlex
import subprocess

SRC = Path('/Volumes/McLuhan/Movies/tv shows')
TARGET = Path('/Users/tom/Documents')
DIR = (
    'Northern Exposure  - (Complete Series with Original Music)'
    ' - H265.HEVC.AC3.256kbps/'
)
SROOT = SRC / DIR
TROOT = TARGET / DIR
SEASONS = sorted(d for d in SROOT.iterdir() if d.is_dir())
assert len(SEASONS) == 6, len(SEASONS)


def copy():
    cmds = []
    count = 0
    for season in SEASONS:
        for src in sorted(e for e in season.iterdir() if e.suffix == '.mkv'):
            count += 1
            target = TARGET / src.relative_to(SROOT).with_suffix('.mp4')
            target.parent.mkdir(parents=True, exist_ok=True)

            cmd = (
                'ffmpeg', '-i', str(src),
                '-c:v', 'h264_videotoolbox', '-b:v', '960k',
                str(target)
            )
            print(src.stem.removeprefix('Northern Exposure - '))
            cmds.append(shlex.join(cmd))
        print()

    print()
    print(*cmds, sep='\n')


if __name__ == '__main__':
    copy()
