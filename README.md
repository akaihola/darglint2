# Darglint2

A functional docstring linter which checks whether a docstring's
description matches the actual function/method implementation.
*Darglint2* expects docstrings to be formatted using the
[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html),
or [Sphinx Style Guide](https://pythonhosted.org/an_example_pypi_project/sphinx.html#function-definitions),
or [Numpy Style Guide](https://numpydoc.readthedocs.io/en/latest/format.html).

Feel free to submit an issue/pull request if you spot a problem or
would like a feature in *darglint2*.

**Table of Contents**:

- [Project Status](#project-status)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Scope](#scope)
- [Sphinx](#sphinx)
- [Numpy](#numpy)
- [Integrations](#integrations)
- [Flake8](#flake8)
- [Roadmap](#roadmap)
- [Contribution](#development-and-contributions)


## Project Status

This is a renamed fork of the original
[darglint](https://github.com/terrencepreilly/darglint) by
[@terrencepreilly](https://github.com/terrencepreilly), and I'm maintaining it
and accepting bugfixes.


## Installation

To install *darglint2*, use pip.

```bash
pip install darglint2
```

Or, clone the repository, `cd` to the directory, and

```bash
pip install .
```

## Configuration

*darglint2* can be configured using a configuration file.  The configuration
file must be named either *.darglint2*, *.darglint*, *setup.cfg*, or *tox.ini*.  It must
also have a section starting with the section header, `[darglint2]`.
Finally, the configuration file must be located either in the directory
*darglint2* is called from, or from a parent directory of that working
directory.

Currently, the configuration file allows us to ignore errors, to specify
message templates, to specify the strictness of checks and to ignore common
exceptions.

### Error Configuration

If we would like to ignore `ExcessRaiseError`s (because we know that
an underlying function will raise an exception), then we would add its
error code to a file named *.darglint2*:

```ini
[darglint2]
ignore=DAR402
```

We can ignore multiple errors by using a comma-separated list:

```ini
[darglint2]
ignore=DAR402,DAR103
```

Instead of specifying error codes to ignore in general one can also specify a
regex to exclude certain function names from tests. For example, the following 
configuration would disable linting on all private methods.
```ini
[darglint2]
ignore_regex=^_(.*)
```

### Message Template Configuration

If we would like to specify a message template, we may do so as
follows:

```ini
[darglint2]
message_template={msg_id}@{path}:{line}
```

Which will produce a message such as `DAR102@driver.py:72`.

Finally, we can specify the docstring style type using `docstring_style`
("google" by default):

```ini
[darglint2]
docstring_style=sphinx
```

### Strictness Configuration

Strictness determines how lax darglint2 will be when checking docstrings.
There are three levels of strictness available:

- short: One-line descriptions are acceptable; anything
more and the docstring will be fully checked.

- long: One-line descriptions and descriptions without
arguments/returns/yields/etc. sections will be allowed.  Anything more,
and the docstring will be fully checked.

- full: (Default) Docstrings will be fully checked.

For example, if we have the following function:

```python
def double(x):
    # <docstring>
    return x * 2
```

Then the following table describes which errors will be raised for
each of the docstrings (rows) when checked against each of the
configurations (columns):

```
┌──────────────────────────────┬──────────────────┬────────────────┬──────────────────┐
│ Docstring                    │  short           │  long          │  full            │
├──────────────────────────────┼──────────────────┼────────────────┼──────────────────┤
│ """Doubles the argument."""  │ None             │ None           │ Missing argument │
│                              │                  │                │ Missing return   │
│                              │                  │                │                  │
│                              │                  │                │                  │
├──────────────────────────────┼──────────────────┼────────────────┼──────────────────┤
│ """Doubles the argument.     │ Missing argument │ None           │ Missing argument │
│                              │ Missing return   │                │ Missing return   │
│ Not very pythonic.           │                  │                │                  │
│                              │                  │                │                  │
│ """                          │                  │                │                  │
│                              │                  │                │                  │
├──────────────────────────────┼──────────────────┼────────────────┼──────────────────┤
│ """Doubles the argument.     │ Missing return   │ Missing return │ Missing return   │
│                              │                  │                │                  │
│ Args:                        │                  │                │                  │
│     x: The number to double. │                  │                │                  │
│                              │                  │                │                  │
│ """                          │                  │                │                  │
└──────────────────────────────┴──────────────────┴────────────────┴──────────────────┘
```

In short, if you want to be able to have single-line docstrings, and check
all other docstrings against their described parameters, you would specify

```ini
[darglint2]
strictness=short
```

In your configuration file.

### Ignoring common exceptions

We can specify a list of exceptions that don't need to be documented in the
raises section of a docstring. For example,

```ini
[darglint2]
ignore_raise=ValueError,MyCustomError
```

### Logging

When *darglint2* fails unexpectedly, you can try to gather more
information when submitting a bug by running with logging.
For example,

```bash
darglint2 --log-level=INFO unexpected_failures.py
```

*Darglint2* accepts the levels, `DEBUG`, `INFO`, `WARNING`, `ERROR`, and
`CRITICAL`.


## Usage


### Command Line use

Given a python source file, `serializers.py`, you would check the docstrings
as follows:

```bash
darglint2 serializers.py
```

You can give an optional verbosity setting to *darglint2*.  For example,

```bash
darglint2 -v 2 *.py
```

Would give a description of the error along with information as to this
specific instance.  The default verbosity is 1, which gives the filename,
function name, line number, error code, and some general hints.

To use an arbitrary error format, you can pass a message template, which
is a python format string.  For example, if we pass the message
template

```bash
darglint2 -m "{path}:{line} -> {msg_id}" darglint2/driver.py
```

Then we would get back error messages like

```bash
darglint2/driver.py :61 -> DAR101
```

The following attributes can be passed to the format string:
- *line*: The line number,
- *msg*: The error message,
- *msg_id*: The error code,
- *obj*: The function/method name,
- *path*: The relative file path.

The message template can also be specified in the configuration file
as the value `message_template`.

*darglint2* is particularly useful when combined with the utility, `find`.
This allows us to check all of the files in our project at once.  For example,
when eating my own dogfood (as I tend to do), I invoke *darglint2* as follows:

```bash
find . -name "*.py" | xargs darglint2
```

Where I'm searching all files ending in ".py" recursively from the
current directory, and calling *darglint2* on each one in turn.

### Ignoring Errors in a Docstring

You can ignore specific errors in a particular docstring.  The syntax
is much like that of *pycodestyle*, etc.  It generally takes the from
of:

```python
# noqa: <error> <argument>
```

Where `<error>` is the particular error to ignore (`DAR402`, or `DAR201`
for example), and `<argument>` is what (if anything) the ignore
statement refers to (if nothing, then it is not specified).

Let us say that we want to ignore a missing return statement
in the following docstring:

```python
def we_dont_want_a_returns_section():
  """Return the value, 3.

  # noqa: DAR201

  """
  return 3
```

We put the `noqa` anywhere in the top level of the docstring.
However, this won't work if we are missing something more specific,
like a parameter.  We may not want to ignore all missing parameters,
either, just one particular one.  For example, we may be writing a
function that takes a class instance as self. (Say, in a bound *celery*
task.) Then we would do something like:

```python
def a_bound_function(self, arg1):
  """Do something interesting.

  Args:
    arg1: The first argument.

  # noqa: DAR101 arg1

  """
  arg1.execute(self)
```

So, the argument comes to the right of the error.

We may also want to mark excess documentation as being okay.  For example,
we may not want to explicitly catch and raise a `ZeroDivisionError`.  We
could do the following:

```python
def always_raises_exception(x):
    """Raise a zero division error or type error.o

    Args:
      x: The argument which could be a number or could not be.

    Raises:
      ZeroDivisionError: If x is a number.  # noqa: DAR402
      TypeError: If x is not a number.  # noqa: DAR402

    """
    x / 0
```

So, in this case, the argument for `noqa` is really all the way to
the left.  (Or whatever description we are parsing.)  We could also
have put it on its own line, as `# noqa: DAR402 ZeroDivisionError`.

### Type Annotations

Darglint2 parses type annotations in docstrings, and can, optionally,
compare the documented type to the actual type annotation.  This can
be useful when migrating a codebase to use type annotations.

In order to make these comparisons, Darglint2 only accepts types
accepted by Python (see [PEP 484](https://www.python.org/dev/peps/pep-0484/).)
That is, it does not accept parentheses in type signatures. (If
parentheses are used in the type signature, Darglint2 will mark that
argument as missing.  See Issue #90.)


### Error Codes

- *DAR001*: The docstring was not parsed correctly due to a syntax error.
- *DAR002*: An argument/exception lacks a description
- *DAR003*: A line is under-indented or over-indented.
- *DAR004*: The docstring contains an extra newline where it shouldn't.
- *DAR005*: The item contains a type section (parentheses), but no type.
- *DAR101*: The docstring is missing a parameter in the definition.
- *DAR102*: The docstring contains a parameter not in function.
- *DAR103*: The docstring parameter type doesn't match function.
- *DAR104*: (disabled) The docstring parameter has no type specified 
- *DAR105*: The docstring parameter type is malformed.
- *DAR201*: The docstring is missing a return from definition.
- *DAR202*: The docstring has a return not in definition.
- *DAR203*: The docstring parameter type doesn't match function.
- *DAR301*: The docstring is missing a yield present in definition.
- *DAR302*: The docstring has a yield not in definition.
- *DAR401*: The docstring is missing an exception raised.
- *DAR402*: The docstring describes an exception not explicitly raised.
- *DAR501*: The docstring describes a variable which is not defined.

The number in the hundreds narrows the error by location in the docstring:

- 000: Syntax, formatting, and style
- 100: Args section
- 200: Returns section
- 300: Yields section
- 400: Raises section
- 500: Variables section

You can enable disabled-by-default exceptions in the configuration file
using the `enable` option.  It accepts a comma-separated list of error
codes.

```ini
[darglint2]
enable=DAR104
```

## Scope

Darglint2's primary focus is to identify incorrect and missing documentationd
of a function's signature. Checking style is a stretch goal, and is supported
on a best-effort basis.  Darglint2 does not check stylistic preferences expressed
by tools in the Python Code Quality Authority (through tools such as `pydocstyle`).
So when using Darglint2, it may be a good idea to also use `pydocstyle`, if you
want to enforce style.  (For example, `pydocstyle` requires the short summary
to be separated from other sections by a line break.  Darglint2 makes no such check.)

## Sphinx

Darglint2 can handle sphinx-style docstrings, but imposes some restrictions
on top of the Sphinx style. For example, all fields (such as `:returns:`)
must be the last items in the docstring.  They must be together, and all
indents should be four spaces.  These restrictions may be loosened at a
later date.

To analyze Sphinx-style docstrings, pass the style flag to the command:

```bash
darglint2 -s sphinx example.py
darglint2 --docstring-style sphinx example.py
```

Alternatively, you can specify the style in the configuration file using
the setting, "docstring\_style":

```ini
[darglint2]
docstring_style=sphinx
```

## Numpy

Darglint2 now has an initial implementation for Numpy-style docstrings.
Similarly to Sphinx-style docstrings, you can pass a style flag to the
command:

```bash
darglint2 -s numpy example.py
darglint2 --docstring-style numpy example.py
```

Or set it in a configuration file:

```ini
[darglint2]
docstring_style=numpy
```

The numpy parser and error reporter are not yet fully stabilized.
Add issues or suggestions to the tracking bug, Issue #69.

## Integrations

### Flake8

Darglint2 can be used in conjunction with Flake8 as a plugin.  The only
setup necessary is to install Flake8 and Darglint2 in the same environment.
Darglint2 will pull its configuration from Flake8. So, if you would like to
lint Sphinx-style comments, then you should have `docstring_style=sphinx` in a
Flake8 configuration file in the project directory.  The settings would
be entered under the flake8 configuration, not a separate configuration
for Darglint2.  E.g.:

```ini
[flake8]
strictness=short
docstring_style=sphinx
```

To see which options are exposed through Flake8, you can check the Flake8
tool:

```bash
flake8 --help | grep --before-context=2 Darglint2
```

### SublimeLinter

A plugin for SublimeLinter can be found [here](https://github.com/raddessi/SublimeLinter-contrib-darglint).
Note that it was built for the original `darglint`, not `darglint2`, and its
compatibility with `darglint2` is yet to be verified.

### Pre-commit

Download [pre-commit](https://pre-commit.com/) and
[install](https://pre-commit.com/#install) it. Once it is installed, add this
to `.pre-commit-config.yaml` in your repository:

```yaml
repos:
-   repo: https://github.com/akaihola/darglint2
    rev: master
    hooks:
    - id: darglint2
```

Then run `pre-commit install` and you're ready to go. Before commiting,
`darglint2` will be run on the staged files. If it finds any errors, the user
is notified and the commit is aborted. Store necessary configuration (such as
error formatting) in `.darglint2`, `.darglint`, `setup.cfg` or `tox.ini`.


## Roadmap

Below are some of the features or efforts from the original `darglint` project
at the time of forking in February 2023.  Where a milestone or
issue is associated with the idea, it will be mentioned.  Some of these
ideas were moonshots and may not get implemented.  They are ordered
roughly according to priority/feasibility stated by the original author.

- [ ] Expose command-line options through sphinx.
- [ ] Robust logging for errors caused/encountered by *darglint2*.
- [ ] Check class docstrings (See
      [darglint#25](https://github.com/terrencepreilly/darglint/issues/25)).
- [ ] Autoformatting docstrings. (See
      [darglint milestone #3](https://github.com/terrencepreilly/darglint/milestone/3)).
- [ ] Optional aggressive style checking through command line flag.
- [ ] ALE support.
- [ ] Syntastic support. (Syntastic is not accepting new checkers until
their next API stabilizes, so this may take some time.)


## Development and Contributions

### Development Setup

Install `darglint2`. First, clone the repository:

```bash
git clone https://github.com/akaihola/darglint2.git
```

`cd` into the directory, create a virtual environment (optional), then setup:

```bash
cd darglint2/
virtualenv -p python3.6 .env
source .env/bin/activate
pip install -e .
```

You can install dependencies using

```bash
pip install poetry
poetry install
```

You can run the tests using

```bash
python setup.py test
```

Or, install `pytest` manually, `cd` to the project's root directory,
and run

```bash
pytest
```

This project tries to conform by the styles imposed by `pycodestyle`
and `pydocstyle`, as well as by `darglint2` itself.


A dockerfile exists for testing with Python3.4.  Although it's not
officially supported (only 3.6+), it's nice to try to make minor
version numbers support it.  You would build the dockerfile and
test using something like

```bash
pushd docker-build
docker build -t darglint2-34 -f Dockerfile.test34 .
popd
docker run -it --rm -v $(pwd):/code darglint2-34 pytest
```

### Contribution

If you would like to tackle an issue or feature, email me or comment on the
issue to make sure it isn't already being worked on.  Contributions will
be accepted through pull requests.  New features should include unit tests,
and, of course, properly formatted documentation.

Also, check out the wiki prior to updating the grammar.  It includes a
description of darglint2's parsing pipline.
