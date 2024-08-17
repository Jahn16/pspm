# `run`

Runs a command installed in the project's virtual env. This command loads env variables from a `.env` file

> [!NOTE]
> This command searches for executables in the `.venv/bin` directory

## Arguments

- `command`: Command to execute
- `arguments`: Arguments to pass to command

## Examples

Run an executable installed inside the virtual env:

```bash
rye run ruff format src/
```
