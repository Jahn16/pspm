## [`Poetry`](https://python-poetry.org/), [`PDM`](https://python-poetry.org/)

Those are great tools, much more powerful than `pspm`. My problem with those is that they add proprietary configuration in the `pyproject.toml` and generate proprietary lock files as well. That means they must be installed in the production environment and every developer is obligated to use them.

## [`rye`](https://rye.astral.sh/)

My favourite of the bunch, `pspm` was heavily inspired by this project. It adds few proprietary configuration and creates a `pip` compatible lock file, meaning you don't have to install in production. I just have a few problems with it: every developer still must use it and the lock file includes the current project, meaning installing only the dependencies is a bit of hassle.

## `pspm`

Does not add any properietary configuration to `pyproject.toml` and generates a `pip` compatible lock file. It is faster than the aforementioned `Poetry`, `PDM` because it uses [`uv`](https://rye.astral.sh/uv/) to manage dependencies[^1]. Allows users to use custom initial templates[^2], see [`Working with Templates`](templates.md). And, has the prettier user interface because it's powered by [`Typer`](https://rye.astral.sh/).

[^1]: As does `rye`
[^2]: As does `PDM`
