# `init`

Create initial project structure. Files created: `pyproject.toml`, `README.md`, `.gitignore`, `src/<NAME>/__init__.py`

## Arguments

- `path`: Where to place the project (defaults to current path)

## Options

- `--name <NAME>`: Project name (defaults to current path basename)
- `--description <DESCRIPTION>`: Project description
- `--not-installable`: If passed pyproject will be created with no `[build-system]` section and the project will not be installed with [`sync`](sync.md)
- `-t`,`--template`: Path to a [copier](https://github.com/copier-org/copier) template, can be a local path or an URL (defaults to [gh:Jahn16/pspm-template](https://github.com/Jahn16/pspm-template))

## Examples

Initialize project in the current directory:

```
~/codes/banana

spm init # Project name will be set to banana
```

Initialize project to another directory:

```
~/codes

spm init apple # Creates directory apple and sets the project name to apple
```

