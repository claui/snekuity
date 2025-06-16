# Contributing to snekuity

## Setting up snekuity for development

To set up snekuity, you need the Python project
management tool [uv](https://docs.astral.sh/uv).

### Installing uv

To install uv, see its
[installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

To verify uv is working, run:

```shell
uv
```

### Setting up your virtual environment

This project uses virtual environments a little differently than most
other projects. Here’s what’s different:

1. Other projects usually let uv automatically pick a managed Python
   and use it to set up the venv transparently.  
   For working on snekuity though, you’ll be using a pre-existing
   Python from your system in which your `gnucash` package lives.  

2. Other projects usually let uv set up a fully isolated venv.  
   For snekuity, you’re going to use a venv as well, but configure it
   with `system-site-packages` so the venv can find the `gnucash`
   package from your system-wide environment.

For the reasons stated, you’re going to tell uv manually how to set up
a venv with the specific configuration you need.

Run the following command line manually, using `-p` to tell uv the path
to the Python executable on your system which can access your `gnucash`
package:

```bash
uv venv --no-managed-python --system-site-packages -p YOUR_PYTHON
```

For example:

```bash
uv venv --no-managed-python --system-site-packages -p /usr/bin/python
```

## Development scripts and tasks

To see a list of available tasks, run: `uv run poe tasks`

### Running the tests

To execute the tests, run:

```shell
uv run poe tests
```

To execute a single test, run e. g.:

```shell
uv run poe tests -vv tests/test_api.py::test_no_incomplete_xacts
```

### Running the linter

To execute the linter, run:

```shell
uv run poe linter
```

### Running the code formatting style check

To check the code base for formatting style violations that are not
covered by the linter, run:

```shell
uv run poe formatcheck
```

### Running the static type check

To execute the static type check, run:

```shell
uv run poe typecheck
```

### Running the entire CI pipeline locally

If you have [act](https://github.com/nektos/act) installed and a
Docker daemon active, run:

```shell
act
```

### Generating project documentation

To generate project documentation (HTML and man page), run:

```shell
uv run poe doc
```

To open the generated HTML documentation in your browser, run:

```shell
uv run poe html
```

To open the generated manual page in your terminal, run:

```shell
uv run poe man
```

## Maintenance

### Refreshing dependencies

If you get errors after a Git pull, refresh your dependencies:

```shell
uv sync
```

### Checking snekuity’s dependencies for compatible updates

To check snekuity’s dependencies for compatible updates, run:

```shell
uv lock -U --dry-run
```

### Updating requirements file for Read the Docs

To update the `doc/requirements.txt` file for Read the Docs, run:

```shell
uv export --only-group doc --output-file doc/requirements.txt
```

### Rebuild `python-snekuity-local` for Arch Linux packaging tests

From a clean Git working tree, run:

```bash
(
  set -ex
  git add -p -- contrib/archlinux/python-snekuity-local/PKGBUILD
  rm -fv contrib/archlinux/python-snekuity-local/*.tar.zst
  env -C contrib/archlinux/python-snekuity-local makepkg -cfs
  git checkout -- contrib/archlinux/python-snekuity-local/PKGBUILD
  namcap contrib/archlinux/python-snekuity-local/PKGBUILD
  sudo pacman -U contrib/archlinux/python-snekuity-local/*.tar.zst
)
```
