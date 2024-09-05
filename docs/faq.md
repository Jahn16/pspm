# FAQ

## Why `pspm` doesn't use version constraints when adding dependencies?

When you're developing a library, it's necessary to support a wide range of versions from your dependencies. Let's suppose that your project depends on a package that is currently in version 4.0.0, it's very likely that everything would work fine with that package in version 3.0.0. What if it didn't? Then set a lower bound in `pyproject.toml`.

But if you're developing an application, you should be using a lock file anyway. So what is the point?

[Good video on this topic](https://www.youtube.com/watch?v=WSVFw-3ssXM)
