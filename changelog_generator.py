#!/usr/bin/env python3

import re
import sys
from github import Github, InputGitAuthor


class Generator:
    def __init__(self, repo_name: str, access_token: str, path: str, commit_message: str):
        self.github = Github(access_token)
        self.repo = self.github.get_repo(repo_name)
        self.path = path
        self.commit_message = commit_message

    def get_filtered_commits(self) -> list:
        # feat, fix, docs, lint, refactor, test, chore
        output = []
        for commit in self.repo.get_commits().reversed:
            message = commit.commit.message
            if re.findall(r'^(feat|fix|docs|lint|refactor|test|chore)', message):
                # This prevents automation from artificially increasing changelog size
                if message != self.commit_message:
                    output.append(message)
        return output

    def create_new_changelog(self, commits: list) -> str:
        print("Building changelog based on following commits:\n{}".format(commits))

        changelog = '# Changelog\n\n\n## Features\n\n'

        for feat in commits:
            if re.findall(r'^feat', feat):
                changelog += '* {}\n'.format(feat)

        changelog += '\n## Bugfixes\n\n'

        for fix in commits:
            if re.findall(r'^fix', fix):
                changelog += '* {}\n'.format(fix)

        changelog += '\n## Other changes\n\n'

        for other in commits:
            if re.findall(r'^(docs|lint|refactor|test|chore)', other):
                changelog += '* {}\n'.format(other)

        changelog += '\n\n\n> Changelog generated through the projects\' GitHub Actions.'

        return changelog

    def update_changelog(self):
        commits = self.get_filtered_commits()
        changelog = self.create_new_changelog(commits)
        contents = self.repo.get_contents(self.path)
        author = InputGitAuthor(
            name="github-actions[bot]",
            email="github-actions[bot]@users.noreply.github.com"
        )

        # Don't update changelog when there are no changes
        if contents.decoded_content.decode('utf-8') != changelog:
            print("Updating changelog in remote repository")
            self.repo.update_file(
                path=contents.path,
                message=self.commit_message,
                content=changelog,
                sha=contents.sha,
                committer=author,
                author=author
            )
        else:
            print("New changelog and old changelog are same - update skipped")


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
