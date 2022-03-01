import functools
import subprocess
import sys

run = functools.partial(
    subprocess.run, text=True, capture_output=True, check=True
)

REQUIRED_PACKAGES = ['coreutils', 'sed', 'gawk', 'curl']


def sec_start():
    print('\n----------\n\n')


def run():
    cmd = ('pacman', '-Q') + required_packages
    check_output = run(cmd).stdout.splitlines()

    if deps :=  [p.split("'")[0] for p in check_output]:
        sec_start()

        print('the following dependencies are missing:', *deps)
        yn = input('would you like to install them now? [yes/no]> ').lower()

        if not (yn and yn.lower()[0] == 'y'):
            return 'install missing dependencies!'

        run(['pacman', '-S', '--noconfirm'] + missing_dependencies)


if __name__ == '__main__':
    sys.exit(run)
