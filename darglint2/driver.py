"""Defines the command line interface for darglint2."""
import argparse
import ast
import inspect
import pathlib
import sys
from typing import List

import darglint2.errors
from darglint2.error_report import ErrorReport

from . import __version__
from .config import LogLevel, get_config, get_logger
from .docstring.style import DocstringStyle
from .function_description import get_function_descriptions, read_program
from .integrity_checker import IntegrityChecker
from .strictness import Strictness

# ---------------------- ARGUMENT PARSER -----------------------------

parser = argparse.ArgumentParser(description="Check docstring validity.")
parser.add_argument(
    "--message-template",
    "-m",
    type=str,
    help=(
        "Specify a message template.  This is a Python format string "
        "describing errors, which can access the following attributes:\n"
        "    line: The line number,\n"
        "    msg: The error message,\n"
        "    msg_id: The error code,\n"
        "    obj: The function/method name,\n"
        "    path: The relative file path.\n"
    ),
)
parser.add_argument(
    "--ignore-regex",
    "-i",
    type=str,
    help=(
        "Methods/function names matching this regex will be skipped " "during analysis."
    ),
)
parser.add_argument(
    "--ignore-raise",
    "-c",
    type=str,
    help=(
        "Exceptions that don't need to be documented in docstrings. "
        'Accepts a comma-separated list. E.g.: "ValueError,MyCustomError"'
    ),
)
parser.add_argument(
    "--ignore-properties",
    "-p",
    action="store_true",
    default=False,
    help="Class property methods will be ignored by darglint2",
)
parser.add_argument(
    "--raise-syntax",
    action="store_true",
    help=(
        "When a docstring is incorrectly formatted, raise an exception "
        "rather than storing the error.  Useful for debugging darglint2."
    ),
)
parser.add_argument(
    "--verbosity",
    "-v",
    default=1,
    type=int,
    choices=[1, 2],
    help="The level of verbosity.",
)
parser.add_argument(
    "--version",
    action="store_true",
    help=("Return the current version number of darglint2."),
)
parser.add_argument(
    "files",
    nargs="*",
    help=(
        'The python source files to check. If "-" is given, then stdin will ' "be read."
    ),
)
parser.add_argument(
    "--no-exit-code",
    "-x",
    action="store_true",
    help=(
        "Exit with status 0, even on errors.  By default, darglint2 "
        "exits with status 1 when errors are encountered.  Giving "
        "this flag prevents that.  Useful when invocating with xargs "
        "and you want to see all errors.  "
        'Ex: `find . -name "*.py" | xargs darglint2 -x`'
    ),
)
parser.add_argument(
    "--list-errors",
    action="store_true",
    help=("Print a list of error codes and what they represent."),
)
parser.add_argument(
    "-s",
    "--docstring-style",
    default=None,
    choices=["google", "sphinx", "numpy"],
    help=(
        "The docstring style used in the given project. Currently, "
        "only google, sphinx, and numpy styles are supported."
    ),
)
parser.add_argument(
    "-z",
    "--strictness",
    default=None,
    choices=[
        "short",
        "long",
        "full",
    ],
    help=(
        "The minimum strictness when checking docstrings. "
        "`short`, for example, will result in one-line "
        "docstrings always being accepted.  Anything more than one line "
        "would go through the full check."
    ),
)
parser.add_argument(
    "-e",
    "--enable",
    type=str,
    help=(
        "Enable disabled-by-default errors.  Accepts a "
        "comma-separated list of error codes.  E.g.: "
        '"DAR104,DAR105"'
    ),
)
parser.add_argument(
    "--indentation",
    type=int,
    default=None,
    help=(
        "The number of spaces to count as an indentation. "
        "For example, if following the Google python style "
        "guide, you would set --indentation=2."
    ),
)
parser.add_argument(
    "--log-level",
    "-l",
    type=str,
    default=None,
    choices=[
        "CRITICAL",
        "ERROR",
        "WARNING",
        "INFO",
        "DEBUG",
    ],
    help=(
        "The level at which to log.  Can help with debugging "
        "when something strange is happening.  The default "
        "level, CRITICAL, means that only the most severe of "
        "errors will be logged.  Assertions are logged at the "
        "ERROR level."
    ),
)

# ---------------------- MAIN SCRIPT ---------------------------------


def get_error_report(
    filename: str,
    verbosity: int,
    raise_errors_for_syntax: bool,
    message_template: str = None,
) -> str:
    """Get the error report for the given file.

    Args:
        filename: The name of the module to check.
        verbosity: The level of verbosity, in the range [1, 3].
        raise_errors_for_syntax: True if we want parser errors
            to propagate up (crashing darglint2.)  This is useful
            if we are developing on darglint2 -- we can get the stack
            trace and know exactly where darglint2 failed.
        message_template: A python format string for specifying
            how the message should appear to the user.

    Returns:
        An error report for the file.

    """
    program = read_program(filename)
    try:
        tree = ast.parse(program)
        functions = get_function_descriptions(tree)
        checker = IntegrityChecker(
            raise_errors=raise_errors_for_syntax,
        )
        for function in functions:
            checker.schedule(function)
        return checker.get_error_report_string(
            verbosity,
            filename,
            message_template=message_template,
        )
    except SyntaxError as e:
        error = darglint2.errors.PythonSyntaxError(e)
        report = ErrorReport([error], filename, verbosity, message_template)
        return str(report)


def print_error_list():
    errors: List[str] = list()
    for name, obj in inspect.getmembers(darglint2.errors, inspect.isclass):
        if (
            issubclass(obj, darglint2.errors.DarglintError)
            and obj != darglint2.errors.DarglintError
        ):
            errors.append("{}: {}".format(obj.error_code, obj.description))
    errors.sort()
    print("\n".join(errors))


def print_version():
    print(__version__)


def main() -> None:
    """Run darglint2.

    Called as a script when setup.py is installed.

    """
    args = parser.parse_args()
    exit_code = not args.no_exit_code
    encountered_errors = False

    if args.list_errors:
        print_error_list()
        sys.exit(0)

    if args.version:
        print_version()

    # Expand directories.
    files = []
    for f in args.files:
        p = pathlib.Path(f)
        if not p.is_dir() and p.suffix == ".py":
            files.append(f)
        # Convert back to strings to not require modifications of any
        # subsequent code.
        files.extend(str(i) for i in p.glob("**/*.py"))

    try:
        config = get_config()

        # Only override enable if explicitly passed.
        if args.enable:
            config.enable = [x.strip() for x in args.enable.split(",")]

        if "*" in config.ignore:
            sys.exit(0)

        if args.indentation:
            config.indentation = args.indentation

        if args.docstring_style == "sphinx":
            config.style = DocstringStyle.SPHINX
        elif args.docstring_style == "google":
            config.style = DocstringStyle.GOOGLE
        elif args.docstring_style == "numpy":
            config.style = DocstringStyle.NUMPY

        if args.strictness == "short":
            config.strictness = Strictness.SHORT_DESCRIPTION
        elif args.strictness == "long":
            config.strictness = Strictness.LONG_DESCRIPTION
        elif args.strictness == "full":
            config.strictness = Strictness.FULL_DESCRIPTION

        if args.log_level:
            config.log_level = LogLevel.from_string(args.log_level)

        if args.ignore_regex:
            config.ignore_regex = args.ignore_regex
        if args.ignore_raise:
            config.ignore_raise = [x.strip() for x in args.ignore_raise.split(",")]
        if args.ignore_properties:
            config.ignore_properties = args.ignore_properties

        raise_errors_for_syntax = args.raise_syntax or False
        for filename in files:
            error_report = get_error_report(
                filename,
                args.verbosity,
                raise_errors_for_syntax,
                message_template=args.message_template,
            )
            if error_report:
                print(error_report + "\n")
                encountered_errors = True
    except Exception as exc:
        # Exit with status 129 regardless of whether user wants a
        # exit code or not -- darglint2 failed, and it should
        # look like it failed.
        logger = get_logger()
        logger.critical(exc)
        sys.exit(129)
    if encountered_errors and exit_code:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
