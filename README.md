[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# github-lockify

Simple CLI tool for locking GitHub issues _en masse_.

Handy if you have a project where users keep commenting on old, closed issues and you really want them to stop. 😬

## Install

Requires Python 3, `pip`, and [`requests`](https://docs.python-requests.org):

```sh
$ pip3 install https://github.com/dlenski/github-lockify/archive/master.zip
```

## How to use

You'll need a [GitHub personal access token with repo scope](https://github.com/settings/tokens)
for authentication.

If Github's [`hub` CLI](https://github.com/github/hub) and the [PyYAML](https://pyyaml.org) package are installed,
the script will attempt to use the token from `~/.config/hub`.
(You can manually populate this file with `{"github.com": [{"user": "$USERNAME", "oauth_token": "$TOKEN"}]}` if you prefer.)

If run from a directory containing a Git repository, it will use `git remote -v` to autodetect
the default user and repository from the first `github.com` remote found.

```
$ github-lockify --help
usage: github-lockify [-h] [-u USER] [-t TOKEN] [--do-it]
                      [-r {off-topic,too heated,resolved,spam}] [-U DAYS]
                      [-C DAYS] [--created-age DAYS] [-l LABEL] [-a USERNAME]
                      [-c USERNAME]
                      owner repo

Lock closed GitHub issues en masse.

positional arguments:
  owner                 GitHub repository owner
  repo                  Github repository name

optional arguments:
  -h, --help            show this help message and exit
  --do-it               Actually lock the issues (default is a dry-run where
                        issues are simply listed).
  -r {off-topic,too heated,resolved,spam}, --lock-reason {off-topic,too heated,resolved,spam}
                        Lock-reason to apply (default resolved)

Authentication:
  Not required for a dry-run (except on a private repo), but required to
  actually lock issues.

  -t TOKEN, --token TOKEN
                        GitHub personal access token with repo scope (see
                        https://github.com/settings/tokens).

Selecting closed issues to lock:
  All criteria must match in order for an issue to be locked.

  -U DAYS, --updated-age DAYS
                        Only lock if last UPDATED at least this many days ago
  -C DAYS, --closed-age DAYS
                        Only lock if CLOSED at least this many days ago
  --created-age DAYS    Only lock if CREATED at least this many days ago
  -l LABEL, --label LABEL
                        Only lock if this label is applied (may be specified
                        repeatedly to require multiple labels)
  -a USERNAME, --assignee USERNAME
                        Only lock if assigned to this user ("none" for
                        unassigned)
  -c USERNAME, --creator USERNAME
                        Only lock if created by this user
```

## TODO

* Allow locking open issues?

## License

GPLv3 or later
