# Working with Templates

> [!NOTE]
> Sorry, the following bit is not that simple. In fact, `pspm` bundles with the most powerful template management tool of all package managers.

`PSPM` supports initializing a project from a [copier template](https://github.com/copier-org/copier). By default, the command [`init`](commands/ginit.md) will use [this template](https://github.com/Jahn16/pspm-template), but you can pass your own in the following way:

```
spm init -T gh:Jahn16/pspm-template
```

The template option can be a local path, a Git URL, or a shortcut URL (as shown in the example)

## Creating your own template

You can, and should, create your own template. For that you can fork the [default template](https://github.com/Jahn16/pspm-template), or create one from scratch. In both cases, I would suggest you to read the [copier docs on this topic](https://copier.readthedocs.io/en/latest/creating/).

`PSPM` will pass some data (retrieved from `init` cli options) to `copier` so that the user don't have to fill some information by himself. Those attributes are:

- `project_name`: The project name
- `package_name`: The project name but all lower case and replaced `-` for `_` 
- `is_installable`: Whether the project is installable
- `author_name`, `author_email`: Fetched from git config

I wold suggest you to use the same attributes in your template, but if you want you might change or create other ones in you [`copier.yml`](https://copier.readthedocs.io/en/latest/configuring/#the-copieryml-file) file. This will cause `copier` to prompt the user for missing information.

## Updating a project

Updating a project in very useful if you're adding a new workflow, updating a pre-commit ref, etc. The [`copier update`](https://copier.readthedocs.io/en/latest/updating/) command will sync your project to the updated template.

For that to work you will need to have `copier` installed and a [`.copier-answers.yml`](https://copier.readthedocs.io/en/latest/configuring/#the-copier-answersyml-file) file. Whether this file is created or not is configured in the template. 

> [!WARNING]
> The default template bundled with `pspm` does not create an answers file hence updating is not supported. That means you need to use a custom template to use this feature.
