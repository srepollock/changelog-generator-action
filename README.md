# Changelog Generator Action

A GitHub Action CHANGELOG.md generator.

Generates a changelog based on the commit history. The commit history should follow [Angular](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#type) commit syntax to be effective.

A write up of how to make your own Changelog Generator can be found [on my blog](https://medium.com/@srepollock/).

## Inputs

| Inputs | Description | Required | Default |
| --- | --- | --- | --- |
| REPO_NAME| Repository name | yes | - |
| ACCESS_TOKEN | Github Access Token | yes | You can just pass `${{secrets.GITHUB_TOKEN}}` |
| PATH | Path to the file you want to add contributors' list | no | `/CHANGELOG.md` |
| COMMIT_MESSAGE | commit message | no | `docs(CHANGELOG): update release notes` |

## Outputs

### `changelog`

The changelog file

## Example usage

```yaml
uses: srepollock/changelog-generator-action@master
with:
        REPO_NAME: 'srepollock/changelog-generator-action'
        ACCESS_TOKEN: ${{secrets.GITHUB_TOKEN}}
        PATH: '/CHANGELOG.md'
        COMMIT_MESSAGE: 'docs(CHANGELOG): update release notes'
```

Please see the workflow in `.github/workflows` of this repo to see how the job steps are setup.

> By Spencer Pollock <spencer@spollock.ca>
