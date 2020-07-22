# Changelog Generator Action

A GitHub Action CHANGELOG.md generator.

Generates a changelog based on the commit history. The commit history should follow [Angular](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#type) commit syntax to be effective.

A write up of how to make your own Changelog Generator can be found [on my blog](https://medium.com/@srepollock/).

## Inputs

None

## Outputs

### `changelog`

The changelog file

## Example usage

```
uses: srepollock/changelog-generator-action@master
```

Please see the workflow in `.github/workflows` of this repo to see how the job steps are setup.

> By Spencer Pollock <spencer@spollock.ca>
