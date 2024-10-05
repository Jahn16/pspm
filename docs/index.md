![logo-pspm](https://github.com/user-attachments/assets/6a35d219-1193-42f8-a1b6-0331818e8e4d)

# Introduction

pspm, as described, is a simple Python package manager. It aims to help developers but without getting in their way

## Installation

The recommend installation method is by using [pipx](https://pipx.pypa.io/stable/)

```bash
pipx install pspm[uv]
```

> [!NOTE]
> This will install `pspm` along with `uv`. You may want to [install uv separately](https://docs.astral.sh/uv/getting-started/installation/) and run `pipx install pspm` instead.

## Shell Completion

pspm supports generating completion scripts for Bash, Fish, and Zsh.

```bash
spm --install-completion
```



