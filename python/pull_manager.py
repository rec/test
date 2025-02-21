import argparse
import itertools
from argparse import Namespace
from enum import Enum
from functools import cache, cached_property
from pathlib import Path
from typing import Any, Iterator, Optional, Sequence, Union
import json
import os
import subprocess
import sys

_COMMANDS = {
    "list": "List all pull requests",
    "ref": "Print git ref id of a pull request",
    "url": "Print the URL for a pull request",
}
TOKEN_NAME = "GIT_TOKEN" # "PULL_MANAGER_GIT_TOKEN"
GIT_TOKEN = os.environ.get(TOKEN_NAME)


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

    help = "An optional commit, PR index, pull request, or search (start with :/)"
    parser.add_argument("commit", nargs="?", default=None, help=help)

    help = "The github user name"
    parser.add_argument("--user", "-u", default=None, help=help)

    help = "List all users"
    parsers.list.add_argument("--all", "-a", action="store_true")

    help = "Do a git fetch before anything else"
    parser.add_argument("--fetch", "-f", action="store_true")

    return parser.parse_args()


class PullRef:
    pull: Optional[str] = None
    ref: Optional[str] = None

    def __init__(self, commit: str):
        commit = commit or "HEAD"
        if commit.isnumeric():
            if int(commit) >= 1_000_000:
                self.ref = commit
            else:
                self.pull = commit
        elif pull := commit.partition("#")[2] or commit.partition(_PULL_PREFIX)[2]:
            self.pull = pull
        else:
            try:
                int(commit, 16)
            except ValueError:
                self.ref = commit
            else:
                self.pull = commit


class PullManager:
    def __init__(self, argv=None):
        self.argv = argv

    def __call__(self) -> None:
        if method := getattr(self, f"cmd_{self.args.command}", None):
            method()
        else:
            sys.exit(f"Unimplemented command '{self.args.command}'")

    def _open_pulls(self, user: str):
        commit = self.args.commit
        for ghstack_index in self.all_users[user]:
            try:
                pull, lines, _ref = self._pull_lines_ref(ghstack_index, user=user)
            except Exception as e:
                if not e.args[0].startswith("Cannot find a pull request"):
                    print("ERROR:", e, user, ghstack_index, file=sys.stderr)
                continue
            if (not commit or any(commit in i for i in lines)) and _is_pull_open(pull):
                yield pull, lines

    def cmd_list(self):
        if self.args.all:
            for user in self.all_users:
                for pull, lines in self._open_pulls(user):
                    print(f"{user}: #{pull}: {lines[0]}")
        else:
            for pull, lines in self._open_pulls(self.user):
                print(f"#{pull}: {lines[0]}")

    def cmd_ref(self):
        print(self._pull_ref.pull)

    def cmd_url(self):
        print(f"{_PULL_PREFIX}{self._pull_ref.pull}")

    @cached_property
    def args(self):
        args = parse(self.argv)
        if args.fetch:
            _run("git fetch")
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

    @cached_property
    def all_users(self):
        all_users = {}
        for line in _run("git branch -r"):
            user_gh = line.partition("/gh/")[2]
            if user_gh:
                try:
                    user, ghstack_index, variety = user_gh.split("/")
                except ValueError:
                    continue
                if variety == "orig":
                    all_users.setdefault(user, []).append(ghstack_index)

        return all_users

    @cached_property
    def users(self):
        if getattr(self.args, "all", None):
            return self.all_users
        return {self.user: self.pulls}

    @cached_property
    def pulls(self):
        return self.all_users[self.user]

    @cached_property
    def _pull_ref(self) -> PullRef:
        pr = PullRef(self.args.commit)
        if not pr.pull:
            pr.pull = _ref_to_pull(pr.ref)[0]
            return pr

        refs = []
        search = pr.pull.partition(":/")[2]
        for ghstack_index in self.pulls:
            pull, lines, ref = self._pull_lines_ref(ghstack_index)
            if search and any(search in i for i in lines):
                refs.append(ref)
            elif not search and pull == pr.pull:
                refs.append(ref)

        if not refs:
            raise ValueError(f"Could not find {pr.pull=}")
        if len(refs) > 1:
            raise ValueError(f"Ambiguous {pr.pull=}: {refs}")

        pr.ref = refs[0]
        return pr

    def _pull_lines_ref(self, ghstack_index: str, user: Optional[str] = None) -> tuple[str, list[str], str]:
        ref = self._pull_request_ref(ghstack_index, user)
        pull, lines = _ref_to_pull(ref)
        return pull, lines, ref

    def _pull_request_ref(self, ghstack_index: str, user: Optional[str] = None) -> str:
        return f"upstream/gh/{user or self.user}/{ghstack_index}/orig"


_PULL_PREFIX = "https://github.com/pytorch/pytorch/pull/"


@cache
def _ref_to_pull(ref: str) -> tuple[str, list[str]]:
    lns = _run(f"git log --pretty=medium -1 {ref}")
    it = iter(lns)

    while not (line := next(it)).startswith(" "):
        pass

    lines = [line]
    try:
        while "ghstack-source-id:" not in (line := next(it)):
            lines.append(line)
    except StopIteration:
        raise ValueError(f"{ref=} is not a ghstack commit") from None

    lines = [s for i in lines if (s := i[4:])]

    for i in it:
        if (pull := i.partition(_PULL_PREFIX)[2]):
            return pull, lines
    raise ValueError(f"Cannot find a pull request for {ref=}") from None


def _run_raw(cmd: str):
    try:
        return subprocess.run(
            cmd, capture_output=True, text=True, check=True, shell=True
        ).stdout

    except subprocess.CalledProcessError as e:
        if e.stderr:
            print(f"Error on command `{cmd}`:\n", e.stderr, file=sys.stderr)
        raise

def _run(cmd: str):
    return _run_raw(cmd).splitlines()


def _run_json(cmd: str):
    return json.loads(_run_raw(cmd))


HEADERS = (
    '-H "Accept: application/vnd.github+json" '
    '-H "X-GitHub-Api-Version: 2022-11-28"'
)
URL = "https://api.github.com/repos/pytorch/pytorch/pulls"
if GIT_TOKEN:
    AUTH = f'-H "Authorization: Bearer {GIT_TOKEN}" '
else:
    AUTH = ''
    print(
        f'WARNING: environment variable {TOKEN_NAME} '
        'is not set: github will rate-limit you faster',
        file=sys.stderr
    )
COMMAND = f"curl {HEADERS} {AUTH} {URL}"


@cache
def _is_pull_open(pull: str) -> bool:
    return _run_json(f"{COMMAND}/{pull}")["state"] == "open"


if __name__ == '__main__':
    if True:
        PullManager()()
    else:
        print(_run_raw(f"{COMMAND}/146845"))
