import git, shutil

DIRECTORY = '/tmp/clone'


def clone(url):
    print(url)
    shutil.rmtree(DIRECTORY, ignore_errors=True)
    git.Repo.clone_from(url=url, to_path=DIRECTORY, b='master')


clone('git@:@github.com/ManiacalLabs/BiblioPixelAnimations.git/')
clone('https://:@github.com/ManiacalLabs/BiblioPixelAnimations.git/')
clone('https://:@github.com/ManiacalLabs/NONEXISTENT.git/')
