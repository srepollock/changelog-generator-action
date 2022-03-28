#!/usr/bin/env python3

import re
import shlex
import subprocess
import sys
from github import Github
from github.Repository import Repository


# Use Pygithub to login to the repository
# Reference: https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository
def github_login(access_token: str, repo_name: str) -> Repository:
    g = Github(access_token)
    repo = g.get_repo(repo_name)
    return repo


# Write contributors list to file if it differs
def write_changelog(repo: Repository, changelog: str, path: str, commit_message: str) -> None:
    contents = repo.get_contents(path)
    repo.update_file(contents.path, commit_message, changelog, contents.sha)


def get_commit_log() -> list[str]:
    output = subprocess.check_output(
        shlex.split('git log --pretty=%s --color'), stderr=subprocess.STDOUT)
    output = output.decode('utf-8')
    output = output.split('\n')
    return output


def strip_commits(commits: list) -> list:
    # feat, fix, docs, lint, refactor, test, chore
    output = []
    for line in commits:
        if re.findall(r'^(feat|fix|docs|lint|refactor|test|chore)', line):
            output.append(line)
    return output


def overwrite_changelog(commits: list) -> str:
    print("Going to write the following commits:\n{}".format(commits))

    changelog = '# Changelog\n\n\n## Features\n\n'

    for feat in commits:
        if re.findall(r'^feat', feat):
            changelog += '* {}\n'.format(feat)

        changelog += '\n## Bugfixes\n\n'

    for fix in commits:
        if re.findall(r'^fix', fix):
            changelog += '* {}\n'.format(fix)

    changelog += '\n## Other\n\n'

    for other in commits:
        if re.findall(r'^(docs|lint|refactor|test|chore)', other):
            changelog += '* {}\n'.format(other)

    changelog += '\n\n\n> Changelog generated through the projects\' GitHub Actions.'

    with open("/github/home/CHANGELOG.md", "w+") as file:
        file.write(changelog)
        file.close()

    return changelog


def main():
    repo_name = sys.argv[1]
    access_token = sys.argv[2]
    path = sys.argv[3]
    commit_message = sys.argv[4]

    commits = get_commit_log()
    commits = strip_commits(sorted(commits))
    changelog = overwrite_changelog(commits)

    repo = github_login(access_token, repo_name)
    write_changelog(repo, changelog, path, commit_message)


if __name__ == '__main__':
    main()
