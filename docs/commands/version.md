# `version`

Get or set project version


## Arguments

- `version`: Version to change to

## Options

- `-b, --bump <RULE>`: Bump rule to apply when changing version (`major`, `minor` or `patch`)

## Examples

Get the current version:

```bash
spm version
0.1.0
```

Bump the version by minor:

```bash
spm version -b minor
0.2.0
```

Set to a specific version:

```
spm version 1.0.0
1.0.0
```

