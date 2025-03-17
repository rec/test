import dataclasses as dc
import argparse
from argparse import Namespace
from functools import cache, cached_property
from operator import attrgetter
from pathlib import Path
from typing import Any, Optional, Sequence
import json
import os
from subprocess import run, CalledProcessError
import sys
import webbrowser

_COMMANDS = {
    "commit_url": "Print git ref id URL for a pull request",
    "hud_url": "HUD URL for a pull request",
    "list": "List all pull requests",
    "ref": "Print git ref id of a pull request",
    "ref_url": "Print git ref id URL for a pull request",
    "url": "Print the URL for a pull request",
}
TOKEN_NAMES = "PULL_MANAGER_GIT_TOKEN", "GIT_TOKEN"
GIT_TOKEN = next((token for n in TOKEN_NAMES if (token := os.environ.get(n))), None)
_PULL_PREFIX = "https://github.com/pytorch/pytorch/pull/"
_GHSTACK_SOURCE = "ghstack-source-id:"
_HUD_PREFIX = "https://hud.pytorch.org/pr/"
_PULL_REQUEST_RESOLVED = "Pull Request resolved:"
_REF_PREFIX = "https://github.com/pytorch/pytorch/tree/"
_COMMIT_PREFIX = "https://github.com/pytorch/pytorch/commit/"

FIELDS = "is_open", "pull_message", "pull_number", "ref"
DEBUG = not True

"""
TODO:

* bring in "errors" from elsewhere
* Handle closed pull requests not in a ghstack branch better

"""


class PullError(ValueError):
    pass


@dc.dataclass
class PullRequest:
    ref: str

    @cached_property
    def user(self) -> str:
        return self._user_index[0]

    @cached_property
    def ghstack_index(self) -> int:
        return self._user_index[1]

    @cached_property
    def pull_number(self) -> str:
        return _get_ghstack_message(self.ref)[0]

    @cached_property
    def pull_message(self) -> list[str]:
        return _get_ghstack_message(self.ref)[1]

    @cached_property
    def subject(self) -> str:
        return self.pull_message[0]

    @cached_property
    def is_open(self) -> bool:
        url = f"{_curl_command()}/{self.pull_number}"
        info = _run_json(url)
        if info.get("status") == "404":
            raise ValueError(f"{url=}\n{json.dumps(info, indent=2)}")
        return info["state"] == "open"

    @cached_property
    def commit_id(self) -> str:
        return _run(f"git show-ref -s {self.ref}")[0].strip()

    @cached_property
    def url(self) -> str:
        return f"{_PULL_PREFIX}{self.pull_number}"

    @cached_property
    def commit_url(self) -> str:
        upstream, _, ref = self.ref.partition("/")
        return f"{_COMMIT_PREFIX}{self.commit_id}"

    @cached_property
    def hud_url(self) -> str:
        return f"{_HUD_PREFIX}{self.pull_number}"

    @cached_property
    def ref_url(self) -> str:
        upstream, _, ref = self.ref.partition("/")
        return f"{_REF_PREFIX}{ref}"

    def asdict(self) -> dict[str, Any]:
        return {f: v for f in FIELDS if (v := self.__dict__.get(f)) is not None}

    @classmethod
    def fromdict(cls, ref: str, **kwargs: Any) -> "PullRequest":
        pr = cls(ref)
        pr.__dict__.update(kwargs)
        return pr

    @cached_property
    def _user_index(self) -> tuple[str, int]:
        parts = self.ref.split("/")
        if len(parts) == 5:
            remote, gh, user, index, branch = parts
            if branch != "orig":
                raise PullError("Waiting for orig branch")
            if remote == "upstream" and gh == "gh" and index.isnumeric():
                return user, int(index)

        raise PullError(f"Do not understand git reference '{self.ref}'")


@cache
def _get_ghstack_message(ref: str) -> tuple[str, list[str]]:
    lines = _run(f"git log --pretty=medium -1 {ref}", print_error=False)
    lines = [i[4:] for i in lines if i[:4] == "    "]
    assert lines

    urls = [u for s in lines if (u := s.partition(_PULL_REQUEST_RESOLVED)[2].strip())]
    if not urls:
        raise PullError("not a ghstack pull request")
    if len(urls) > 1:
        raise PullError("Malformed ghstack pull requst")

    end = next((i for i, s in enumerate(lines) if s.startswith(_GHSTACK_SOURCE)), -1)
    lines = lines[:end]
    while lines and not lines[-1].strip():
        lines.pop()
    pull = urls[0].partition(_PULL_PREFIX)[2].strip()
    assert pull.isnumeric() and len(pull) in (6, 7), pull  # We're around 145636 now
    return pull, lines


@dc.dataclass
class PullRequests:
    argv: Optional[Sequence[str]] = None
    path: Path = Path("~/.pull_manager.json").expanduser()

    def load(self) -> None:
        if self.path.exists() and (pulls := json.loads(self.path.read_text())):
            self.pulls = {
                k: [PullRequest.fromdict(**i) for i in v] for k, v in pulls.items()
            }

    def save(self) -> None:
        if (pulls := self.__dict__.get("pulls")) is not None:
            d = {k: [i.asdict() for i in v] for k, v in pulls.items()}
            self.path.write_text(json.dumps(d, indent=2))

    @cached_property
    def pulls(self) -> dict[str, list[PullRequest]]:
        result: dict[str, list[PullRequest]] = {}
        for branch in _run("git branch -r"):
            pr = PullRequest(branch.strip())
            try:
                if self.args.all or pr.user == self.user:
                    result.setdefault(pr.user, []).append(pr)
            except PullError:
                pass
        return result

    def __call__(self) -> None:
        if self.args.fetch:
            _run("git fetch upstream")

        if not (self.args.ignore_cache or self.args.rewrite_cache):
            self.load()

        if self.args.command == "list":
            self._list()
        else:
            value = getattr(self._matching_pull(), self.args.command)
            print(value)
            if self.args.command.endswith("url") and self.args.open:
                webbrowser.open(value)

        if not self.args.ignore_cache:
            self.save()

    def _list(self):
        def clean_and_sort(user: str) -> list[PullRequest]:
            pulls = []
            if user not in self.pulls:
                print(self.pulls)

            for p in self.pulls[user]:
                try:
                    p.pull_number
                    if self.args.search in p.subject and (self.args.closed or p.is_open):
                        pulls.append(p)
                except PullError:
                    pass

            key = attrgetter("subject" if self.args.sort else "pull_number")
            return sorted(pulls, key=key, reverse=self.args.reverse)

        if self.args.all:
            for user in self.pulls.items():
                for p in clean_and_sort(user):
                    print(f"{user}: #{p.pull_number}: {p.subject}")
        else:
            for p in clean_and_sort(self.user):
                print(f"#{p.pull_number}: {p.subject}")

    def _get_pull(self, pull_number: str) -> PullRequest:
        user_pulls = self.pulls.values()
        pulls = (p for pr in user_pulls for p in pr)
        pull_requests_by_number = {p.pull_number: p for p in pulls}
        try:
            return pull_requests_by_number[pull_number]
        except KeyError:
            raise PullError("no pull request") from None

    def _matching_pull(self) -> PullRequest:
        if self.commit.startswith("#"):
            return self._get_pull(self.commit[1:])

        if self.commit.isnumeric() and len(self.commit) < 7:
            return self._get_pull(self.commit)

        try:
            return self._get_pull(_get_ghstack_message(self.commit)[0])
        except CalledProcessError:
            pass

        if pulls := [p for p in self.pulls[self.user] if self.commit in p.subject]:
            return pulls[-1]
        raise PullError("Can't find any matches")

    @cached_property
    def commit(self) -> str:
        return self.args.commit or 'HEAD'

    @cached_property
    def args(self):
        return parse(self.argv)

    @cached_property
    def remotes(self):
        remotes = {}
        for s in _run("git remote -v"):
            remote, url, _ = s.split()
            user = url.partition(":")[2].partition("/")[0]
            remotes[remote] = user

        return remotes

    @cached_property
    def user(self):
        if len(self.remotes) != 1:
            return self.remotes["origin"]
        for r in self.remotes.values():
            return r


def _run_raw(cmd: str, print_error: bool = True):
    try:
        return run(cmd, capture_output=True, text=True, check=True, shell=True).stdout
    except CalledProcessError as e:
        if print_error and e.stderr:
            print(f"Error on command `{cmd}`:\n", e.stderr, file=sys.stderr)
        raise


def _run(cmd: str, print_error: bool = True):
    return _run_raw(cmd, print_error).splitlines()


def _run_json(cmd: str):
    return json.loads(_run_raw(cmd))


@cache
def _curl_command() -> str:
    headers = (
        '-H "Accept: application/vnd.github+json" '
        '-H "X-GitHub-Api-Version: 2022-11-28"'
    )
    url = "https://api.github.com/repos/pytorch/pytorch/pulls"
    if GIT_TOKEN:
        auth = f'-H "Authorization: Bearer {GIT_TOKEN}"'
    else:
        auth = ''
        print(
            f'WARNING: one of environment variable {TOKEN_NAMES} '
            'must be not set or github will rate-limit you sooner',
            file=sys.stderr
        )
    return f"curl {headers} {auth} {url}"


class ArgumentParser(argparse.ArgumentParser):
    """
    Adds better help formatting to argparse.ArgumentParser
    """
    _epilog: str = ""

    def exit(self, status: int = 0, message: Optional[str] = None):
        """
        Overriding this method is a workaround for argparse throwing away all
        line breaks when printing the `epilog` section of the help message.
        """
        argv = sys.argv[1:]
        if self._epilog and not status and "-h" in argv or "--help" in argv:
            print(self._epilog)
        super().exit(status, message)


def parse(argv):
    parser = ArgumentParser()
    add_parser = parser.add_subparsers(help="Commands:", dest="command").add_parser
    parsers = Namespace(**{k: add_parser(k, help=v) for k, v in _COMMANDS.items()})

    # remaining bdeghjklmnpqtvxyz

    for name, p in vars(parsers).items():
        help = "Perform git fetch"
        p.add_argument("--fetch", "-f", action="store_true")

        help = "Ignore cache"
        p.add_argument("--ignore-cache", "-i", action="store_true")

        help = "Rewrite cache"
        p.add_argument("--rewrite-cache", "-w", action="store_true")

        help = "The github user name"
        p.add_argument("--user", "-u", default=None, help=help)

        if name == "list":
            help = "A term to match in git subjects"
            p.add_argument("search", nargs="?", default="", help=help)

            help = "List all users"
            p.add_argument("--all", "-a", action="store_true")

            help = "Also show closed pull requests"
            p.add_argument("--closed", "-c", action="store_true", help=help)

            help = "Reverse order of pull requests"
            p.add_argument("--reverse", "-r", action="store_true", help=help)

            help = "Sort alphabetically"
            p.add_argument("--sort", "-s", action="store_true", help=help)

        else:
            help = "An optional commit, PR index, pull request, or term to search"
            p.add_argument("commit", nargs="?", default="", help=help)

            if name.endswith("url"):
                help = "Open the URL in the browser"
                p.add_argument("--open", "-o", action="store_true", help=help)

    args = sys.argv[1:]
    if "-h" not in args and "--help" not in args:
        if not (args and args[0] and args[0][0] != "-"):
            args = "list", *args

    return parser.parse_args(args)


if __name__ == '__main__':
    try:
        PullRequests()()
    except PullError as e:
        if DEBUG:
            raise
        msg = f'ERROR: {e.args[0]}'
        print(msg)
        sys.exit(-1)
