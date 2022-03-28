#!/usr/bin/env python3

import re
import sys
from github import Github


class Generator:
    def __init__(self, repo_name: str, access_token: str, path: str, commit_message: str):
        self.github = Github(access_token)
        self.repo = self.github.get_repo(repo_name)
        self.path = path
        self.commit_message = commit_message

    def get_filtered_commits(self) -> list:
        # feat, fix, docs, lint, refactor, test, chore
        output = []
        for commit in self.repo.get_commits():
            message = commit.commit.message
            if re.findall(r'^(feat|fix|docs|lint|refactor|test|chore)', message):
                # This prevents automation from artificially increasing changelog size
                if message != self.commit_message:
                    output.append(message)
        return output

    def create_new_changelog(self, commits: list) -> str:
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

        return changelog

    def update_changelog(self):
        commits = sorted(self.get_filtered_commits())
        changelog = self.create_new_changelog(commits)
        contents = self.repo.get_contents(self.path)

        self.repo.update_file(contents.path, self.commit_message, changelog, contents.sha)


def main():
    generator = Generator(
        repo_name=sys.argv[1],
        access_token=sys.argv[2],
        path=sys.argv[3],
        commit_message=sys.argv[4]
    )

    generator.update_changelog()


if __name__ == '__main__':
    main()
