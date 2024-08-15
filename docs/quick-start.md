# Quick Start
## Project Setup

To create a new project use the `spm init` command

```bash
spm init my-project
```

The following structure will be created:

```
my-project/
├── .gitignore
├── pyproject.toml
├── README.md
└── src
    └── my_project
        └── __init__.py
```

## Dependencies

### Add

To add dependencies use the `spm add` command

```bash
spm add pandas
```

### Add with Group
To add dependencies with group use the `--group` option
```bash
spm add -g dev mypy
```

## Run Command

!!! warning
    This will only work for binaries installed inside the virtualenv, like your project script
To run commands using `pspm` use the `spm run` command. This will automatically read your `.env` file

```
spm run my-project
```

## Existing Project

For installing dependencies from a existing project use the `spm install` command. This will install all the dependencies and the package itself

```bash
spm install
```



