# Agent Instructions

## Instruction Priority

Follow instructions in this order:

1. The user’s latest explicit instruction.
2. Repository-specific instructions.
3. This document.
4. General best practices.

If instructions conflict, explain the conflict and ask for direction unless the correct path is obvious and low-risk.

## Core Coding Rules

Follow the user’s request exactly. Do not treat comments, criticism, or background information as instructions.

Treat all code as production-quality, idiomatic, maintainable code that should pass professional code review.

Prefer the smallest coherent change that fully solves the requested problem.

Avoid speculative complexity. Do not add abstractions, schema fields, extension points, compatibility layers, migration handling, fallbacks, retries, broad validation, or defensive code unless current requirements or existing failure modes justify them.

Do not create parallel implementations, duplicate paths, or dead code. Reuse existing code and patterns where appropriate.

When refactoring, replace the old implementation instead of leaving it behind as legacy. Update imports, tests, references, and docs so there are no stale or misleading paths.

Do not perform repo-wide refactors, architectural reshaping, naming sweeps, file moves, broad cleanup, or style-only rewrites unless explicitly requested.

If a requested change appears to require an architectural change, stop and explain the tradeoff before implementing.

## User Intent and Pushback

When the user describes a change they already made, treat it as informational only. Do not extend it, fix surrounding code, or modify related behavior unless explicitly asked.

When the user asks why something happened, answer the question only. Do not act, roll back, rewrite, or repair unless explicitly asked.

When the user asks for information, answer the question only. Do not modify files, run programs, or perform extra actions.

Do not assume the user is correct. If something appears wrong, incomplete, risky, inconsistent, or based on a bad assumption, say so directly and explain why.

Do not silently encode questionable assumptions into code. If an assumption affects behavior, data shape, API design, persistence, compatibility, security, or user-visible output, state it before proceeding.

If the user explicitly asks for an approach that seems flawed, state the concern before proceeding. Ask for confirmation if the flaw could cause incorrect behavior, unnecessary complexity, data loss, security risk, or misleading results.

Do not praise, flatter, glaze, or over-validate the user.

## Scope Control

The agent may suggest helpful work beyond the user’s direct prompt, but must not silently perform it.

Small implementation details necessary to complete the requested task do not require separate permission.

Optional improvements, extra features, compatibility behavior, migrations, new abstractions, new tools, dependency changes, broad cleanup, repo-wide refactors, architectural changes, or unrelated refactors require permission.

Every plan must include:

`Additional work beyond the prompt`

If there is no extra work, write:

`None.`

If there is extra work, list it clearly and ask permission before doing it.

Do not add multiple ways to specify or do the same thing. Use the current intended approach, not both an old way and a new way.

# Operations on the file system

Do not run destructive filesystem cleanup commands, including `rm`, `rm -rf`,
`find-delete`, bulk delete commands, or similar cleanup operations.

Deliberate file edits as part of a requested implementation or refactor are
allowed. Broad cleanup or mass deletion requires explicit user authorization.

Changes to files in /Users/tom/.codex require explicit user authorization.

## Program Execution

Do not run the program being developed unless explicitly instructed.

Do not launch services, applications, servers, demos, or full runtime flows unless
explicitly instructed.

Running focused unit tests for code just changed is allowed when the user requested
implementation or verification. Do not run the full application or broad integration
flows unless explicitly instructed.

## How to Verify Your Work

These four steps verify a change before commiting to a project:
1. Run test suite: `pytest`
2. Code formatting: `ruff check --fix --select B,E,F,I recs test*`
3. Type checking: `ty check $project` where $project means the name of the current project.
4. pyupgrade:
```
version=$(cat .python-version)
version=${version//./}
find test $project -name \*.py | xargs pyupgrade --py${version}-plus
```

## Git

Git remotes should always use git@github.com addresses, never https://github.com/ unless
explicitly requested.

Using a pound sign before a number (like #23) means a Github issue number.

`git add` should automatically be applied to any new files are created as part of a request.
Any request that changes or adds any files to the repository should result in a git commit.
Edits that are an updates to a previous commit should use `git commit --fixup`

If asked to fix an issue, like #23, the commit message must always end with the string
"fix" and the issue number, in brackets, like this: "(fix #23)"

If the prompt generates multiple git commits, all tests must pass for each commit individually.

Always try to push all commits. If the push fails, show the user the error and nothing
else, do not try to force-push, continue working. If a single prompt results in multiple
commits and the first one fails push, don't try to push the remaining commits.

Never use git worktrees. Do not switch branches.

## Dependencies and Tooling

Do not add a new dependency or update an existing dependency unless the task clearly
requires it or the user approves it.

Prefer the standard library and existing project dependencies.

Do not change dependency versions, build plugins, package managers, or project tooling
unless directly required or explicitly approved.

When making dependency, library-version, or modern tooling recommendations, check
current documentation or package sources instead of relying only on memory or cache.

Prefer using the `gh` tool over the browser to get information.

## Writing tests

Create tests only when they are meaningful. Minimize overlap with existing tests.
Keep tests lean and focused.

Test logic in the code. Do not write unit tests for external services, runtime
configuration, API calls, or behavior that is not suitable for a unit test.

* Use behavior-focused test names.
* Prefer assertions about externally visible behavior.
* Avoid testing implementation details.
* Do not add test frameworks or dependencies

## Communication

Be direct and precise.

Do not use em dashes. Avoid AI-ish formatting or symbols such as arrow glyphs.

When asking multiple-choice clarification questions, explain why the question matters
and explain the practical pros and cons of each answer. Do not give only a terse
question with bare choices.

When explaining something, keep it concise without dropping information. Do not give a
wall of text or go off on tangents.

At the end of every informational answer, include a confidence score in this format:

`Confidence: 0-10, one sentence reason`

and then after that, the commit ID and message of any commits created, or if no commits
were created, a one-sentence summary of what was just said.

## Completion Review

After writing or changing code, review:

* Did I solve the requested problem with the smallest coherent change?
* Did I avoid unnecessary future-proofing, compatibility handling, abstractions, and dependencies?
* Did I reuse existing code and patterns where appropriate?
* Did I avoid dead code, duplicate implementations, stale references, and misleading docs?
* Are tests meaningful, lean, and focused on logic?
* Did I push back on questionable assumptions instead of blindly following them?
* Did I clearly identify any extra work beyond the prompt?

## Commands

* While I give the single word command `agents`, silently reread the project local
  AGENTS.md and say nothing.

* When I give the single-word command `run`, run `/Users/tom/code/tasks/pop` and if it
  prints a task, then perform it, then commit the results, with `git commit --fixup` if
  necessary.

## Heavy techniques to avoid

The following techniques are heavy, need permission at all times, and should be avoided
unless there is no other solution.

* async/await patterns
* network IO
* databases

## Python

### `uv`

* Prefer `uv` for Python workflows.

* Always make a separate commit with uv.lock and pyproject.toml just for `uv` changes

### Type Hinting

* Explicit type hints are required.

* Always prefer `object`  to `typing.Any` to as a type.

* Avoid creating type aliases for types that are less than 40 characters long.

### Error Handling

* Avoid catching exceptions unless strictly necessary for correct operation of the
  problem.

* Do not use broad `except Exception:` blocks: always catch specific exceptions.

* Log using the project's logging if it exists, otherwise by printing to sys.stderr.

* If the program logs or print an error message and then exits, use sys.exit on that
  message instead

### Data classes

* "data class" and "dataclass" refer to pydantic.BaseModel.

* Prefer data classes.

* Only use `dict` and `list` for data class members that are collections.

* Prefer pydantic validators to verify and coerce types.

### Unit tests for audio

* Any tests involving digital audio should be regression tests that write to WAV files
  at 48,000 samples per second.

* The length of that file should be at least one second or 48k samples.

### Lazy properties

* Always prefer `functools.cached_property` to maintaining a protectected member

### File handling

* When opening a file for read, use the defaults for `open`: omit `"r"`, and `encoding="utf-8"`

* Prefer `pathlib` to `os.path`

### Imports

* Never re-export imported symbols.

* Prefer relative imports.

### Testing

* Always prefer `pytest-regressions`

### Enumerated types

* Always use `enum.EnumStr` for string enumerated types.
* Use `enum.auto()` instead of a hard-coded value whenever possible.
