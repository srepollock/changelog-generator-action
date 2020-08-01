#!/usr/bin/env python3

import re
import shlex
import subprocess
import time
import sys
import os
from github import Github


def github_login(ACCESS_TOKEN, REPO_NAME):
    '''
    Use Pygithub to login to the repository

    Args:
        ACCESS_TOKEN (string): github Access Token
        REPO_NAME (string): repository name

    Returns:
        github.Repository.Repository: object represents the repo

    References:
    ----------
    [1]https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository
    '''
    g = Github(ACCESS_TOKEN)
    repo = g.get_repo(REPO_NAME)
    return repo


def get_inputs(input_name):
    '''
    Get a Github actions input by name

    Args:
        input_name (str): input_name in workflow file

    Returns:
        string: action_input

    References
    ----------
    [1] https://help.github.com/en/actions/automating-your-workflow-with-github-actions/metadata-syntax-for-github-actions#example
    '''
    return os.getenv('INPUT_{}'.format(input_name).upper())


def write_changelog(repo, changelog, path, commit_message):
    '''
    Write contributors list to file if it differs

    Args:
        repo (github.Repository.Repository): object represents the repo
        changelog (string): content of changelog
        path (string): the file to write
        commit_message (string): commit message
    '''
    contents = repo.get_contents(path)
    repo.update_file(contents.path, commit_message, changelog, contents.sha)


def get_commit_log():
    output = subprocess.check_output(
        shlex.split('git log --pretty=%s --color'), stderr=subprocess.STDOUT)
    output = output.decode('utf-8')
    output = output.split('\n')
    return output


def strip_commits(commits):
    # feat, fix, refactor, test
    output = []
    for line in commits:
        if re.findall(r'^(feat|fix|refactor|test|ci)', line):
            output.append(line)
    return output


def overwrite_changelog(commits):
    print("Going to write the following commits:\n{}".format(commits))
    changelog = ''
    with open("/github/home/CHANGELOG.md", "w+") as file:
        file.write('# Changelog\n\n\n## Features\n\n')
        changelog += '# Changelog\n\n\n## Features\n\n'
        for feat in commits:
            if re.findall(r'^feat', feat):
                file.write('* {}\n'.format(feat))
                changelog += '* {}\n'.format(feat)
        file.write('\n## Bugs\n\n')
        changelog += '\n## Bugs\n\n'
        for fix in commits:
            if re.findall(r'^fix', fix):
                file.write('* {}\n'.format(fix))
                changelog += '* {}\n'.format(fix)
        file.write('\n## Other\n\n')
        changelog += '\n## Other\n\n'
        for other in commits:
            if re.findall(r'^(refactor|test|ci)', other):
                file.write('* {}\n'.format(other))
                changelog += '* {}\n'.format(other)
        file.write(
            '\n\n\n> Changelog generated through the projects\' GitHub Actions.'
        )
        changelog += '\n\n\n> Changelog generated through the projects\' GitHub Actions.'
        file.close()
    return changelog


def main():
    ACCESS_TOKEN = get_inputs('ACCESS_TOKEN')
    REPO_NAME = get_inputs('REPO_NAME')
    PATH = get_inputs('PATH')
    COMMIT_MESSAGE = get_inputs('COMMIT_MESSAGE')
    commits = get_commit_log()
    commits = strip_commits(sorted(commits))
    changelog = overwrite_changelog(commits)
    repo = github_login(ACCESS_TOKEN, REPO_NAME)
    write_changelog(repo, changelog, PATH, COMMIT_MESSAGE)


if __name__ == '__main__':
    main()
