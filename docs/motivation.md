1. In Python's ecosystem there is no de facto standard package manager, like Cargo for Rust or Go Modules for Go. That's a problem because when you choose a package manager for your Python project you force all the other mantainers to use the same one, with all its strange gimmicks. That's why `pspm` is designed in a way that if you don't want it, you can just not use it.
2. You don't need a package manager. Python is there since 1991 and just in 2018-2020 those famous package managers like `poetry`, `pdm` were created. What you really need is a way of locking your dependencies and for that that are awesome tools like [pip-tools](https://github.com/jazzband/pip-tools) and [uv](https://github.com/jazzband/pip-tools). In fact, `pspm` is just a wrapper for running `uv` commands but you could as well run those commands mannualy or with `pre-commit`, `CI`.

---
Since you are here, you might as well watch this video from Anthony, creator of pre-commit, pytest, and others. This page is highly inspired by his video.

<iframe width="560" height="315" src="https://www.youtube.com/embed/Gr9o8MW_pb0?si=uOvNqU9lLPhykqm3" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
