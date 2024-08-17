# `add`

Adds package to pyproject, installs it and lock version

## Arguments

- `package`: Package to install

## Options

- `-g`,`--group`: The group to add dependency to (it will be inserted in the `[project.optional-dependencies.<group>]` pyproject section)

## Examples

Install dependency to group:

```bash
spm add -g docs mkdocs
```
