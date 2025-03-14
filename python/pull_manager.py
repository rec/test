import dataclasses as dc
import argparse
import itertools
from argparse import Namespace
from enum import Enum
from functools import cache, cached_property
from pathlib import Path
from typing import Any, Iterator, Optional, Sequence, Union
import json
import os
from subprocess import run, CalledProcessError
import sys

_COMMANDS = {
    "hud": "HUD URL for a pull request",
    "list": "List all pull requests",
    "ref": "Print git ref id of a pull request",
    "url": "Print the URL for a pull request",
}
TOKEN_NAMES = "PULL_MANAGER_GIT_TOKEN", "GIT_TOKEN"
GIT_TOKEN = next((token for n in TOKEN_NAMES if (token := os.environ.get(n))), None)
_PULL_PREFIX = "https://github.com/pytorch/pytorch/pull/"
_HUD_PREFIX = "https://hud.pytorch.org/pr/"

FIELDS = "is_open", "pull_message", "pull_number", "ref"


class PullError(ValueError):
    pass


@dc.dataclass
class PullRequest:
    ref: str

    @classmethod
    def make(cls, ref: str) -> Optional['PullRequest']:
        try:
            return cls(ref.strip())
        except PullError:
            return None

    @cached_property
    def user(self) -> str:
        return self._user_index[0]

    @cached_property
    def ghstack_index(self) -> int:
        return self._user_index[1]

    @cached_property
    def pull_number(self) -> str:
        return _get_pull_number_and_message(self.ref)[0]

    @cached_property
    def pull_message(self) -> list[str]:
        return _get_pull_number_and_message(self.ref)[1]

    @cached_property
    def subject(self) -> str:
        return self.pull_message[0]

    @cached_property
    def is_open(self) -> bool:
        info = _run_json(f"{_curl_command()}/{self.pull_number}")
        return info["state"] == "open"

    @cached_property
    def url(self) -> str:
        return f"{_PULL_PREFIX}{self.pull_number}"

    @cached_property
    def hud_url(self) -> str:
        return f"{_HUD_PREFIX}{self.pull_number}"

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
            remote, gh, user, index, _ = parts
            if remote == "upstream" and gh == "gh" and index.isnumeric():
                return user, int(index)

        raise PullError(f"Do not understand git reference '{self.ref}'")


@cache
def _get_pull_number_and_message(ref: str) -> tuple[str, list[str]]:
    it = iter(_run(f"git log --pretty=medium -1 {ref}"))

    while not (line := next(it)).startswith(" "):
        pass

    lines = [line]
    try:
        while "ghstack-source-id:" not in (line := next(it)):
            lines.append(line)
    except StopIteration:
        raise PullError(f"{ref=} is not a ghstack commit") from None

    lines = [s for i in lines if (s := i[4:])]

    for i in it:
        if (pull := i.partition(_PULL_PREFIX)[2]):
            return pull, lines
    raise PullError(f"Cannot find a pull request for {ref=}")


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
            if pr := PullRequest.make(branch):
                result.setdefault(pr.user, []).append(pr)
        return result

    def __call__(self) -> None:
        if not (method := getattr(self, f"cmd_{self.args.command}", None)):
            sys.exit(f"Unimplemented command '{self.args.command}'")

        if self.args.refresh:
            _run("git fetch")
        else:
            self.load()
        method()
        self.save()

    def cmd_list(self):
        if self.args.all:
            for user, pulls in self.pulls.items():
                for p in pulls:
                    if self.args.match in p.subject:
                        print(f"{user}: #{p.pull_number}: {p.subject}")
        else:
            for p in self.pulls[self.user]:
                print(f"#{p.pull_number}: {p.subject}")

    def cmd_ref(self):
        print(self._matching_pull().ref)

    def cmd_url(self):
        print(self._matching_pull().url)

    def _get_pull(self, pull_number: str) -> PullRequest:
        user_pulls = self.pulls.values()
        pulls = (p for pr in user_pulls for p in pr)
        pull_requests_by_number = {p.pull_number: p for p in pulls}
        try:
            return pull_requests_by_number[pull_number]
        except KeyError:
            raise ValueError(f"No pull request {self.commit}") from None

    def _matching_pull(self) -> PullRequest:
        if self.commit.startswith("#"):
            return self._get_pull(self.commit[1:])

        if self.commit.isnumeric() and len(self.commit) < 7:
            return self._get_pull(self.commit)

        try:
            return self._get_pull(_get_pull_number_and_message(self.commit)[0])
        except CalledProcessError as e:
            pass

        pulls = [p for p in self.pulls[self.user] if self.commit in p.subject]
        if len(pulls) == 1:
            return pulls[0]

        if not pulls:
            raise ValueError(f"Can't find any matches for {self.commit}")

        mat = ", ".join(p.pull_number for p in pulls)
        raise ValueError(f"Multiple matches for {self.commit}: {mat}")

    @cached_property
    def commit(self) -> str:
        return self.args.commit or 'HEAD'

    @cached_property
    def args(self):
        return parse(self.argv)
        if args.fetch:
            _run("git fetch") # elsewhere!
        return args

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


def _run_raw(cmd: str):
    try:
        return run(cmd, capture_output=True, text=True, check=True, shell=True).stdout
    except CalledProcessError as e:
        if e.stderr:
            print(f"Error on command `{cmd}`:\n", e.stderr, file=sys.stderr)
        raise


def _run(cmd: str):
    return _run_raw(cmd).splitlines()


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

    help = "A term to match in git subjects"
    parsers.list.add_argument("match", nargs="?", default="", help=help)

    help = "An optional commit, PR index, pull request, or search"
    for p in (parsers.ref, parsers.url, parsers.hud):
        p.add_argument("commit", nargs="?", default="", help=help)

    help = "The github user name"
    parser.add_argument("--user", "-u", default=None, help=help)

    help = "List all users"
    parsers.list.add_argument("--all", "-a", action="store_true")

    help = "Refresh everything from github, including git fetch"
    parser.add_argument("--refresh", "-r", action="store_true")

    return parser.parse_args()


if __name__ == '__main__':
    PullRequests()()
