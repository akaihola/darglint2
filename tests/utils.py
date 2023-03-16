import random
import string
import sys
from typing import Callable, Iterable, List, Set
from unittest import skip

from darglint2.token import Token, TokenType

REFACTORING_COMPLETE = True


def require_python(major=3, minor=8):
    """Skip a unit test if the python version is too old.

    Args:
        major: The major python version.
        minor: The minor python version.

    Returns:
        The function, possibly wrapped by `skip`.

    """

    def _wrapper(fn):
        if sys.version_info.major < major:
            return skip(fn)
        if sys.version_info.minor < minor:
            return skip(fn)
        return fn

    return _wrapper


def replace(name: str = "") -> Callable:
    """Decorates a function which must be replaced.

    If the above global, REFACTORING_COMPLETE is True,
    then it will fail if no alternate is defined for
    it.

    Args:
        name: The name of the method which is replacing it.

    Returns:
        The same function, failing if the refactoring is complete.

    """

    def wrapper(fn: Callable) -> Callable:
        def _inner(*args, **kwargs):
            self = args[0]
            if not hasattr(self, name) and REFACTORING_COMPLETE:
                self.fail("No replacement defined!")
            return fn(*args, **kwargs)

        return _inner

    return wrapper


def remove(fn: Callable) -> Callable:
    """Describes a method which should be removed after refactoring.

    Args:
        fn: The method which should be removed.

    Returns:
        A method which will fail if refactoring has completed.

    """

    def _inner(*args, **kwargs):
        if REFACTORING_COMPLETE:
            self = args[0]
            self.fail("This should have been removed!")
        return fn(*args, **kwargs)

    return _inner


def random_string(min_length: int = 1, max_length: int = 20) -> str:
    ret = ""
    for i in range(random.randint(min_length, max_length)):
        ret += random.choice(string.ascii_letters)
    return ret


def random_tokens(
    min_length: int = 1, max_length: int = 20, exclude: Set[TokenType] = set()
) -> Iterable[Token]:
    allowable = [x for x in TokenType if x not in exclude]
    ret: List[Token] = list()
    line_number = 0
    for i in range(random.randint(min_length, max_length)):
        _type: TokenType = random.choice(allowable)
        if _type == TokenType.ARGUMENTS:
            value = "Args"
        elif _type == TokenType.COLON:
            value = ":"
        elif _type == TokenType.DOCTERM:
            value = '"""'
        elif _type == TokenType.HASH:
            value = "#"
        elif _type == TokenType.INDENT:
            value = "    "
        elif _type == TokenType.LPAREN:
            value = "("
        elif _type == TokenType.NEWLINE:
            value = "\n"
        elif _type == TokenType.RAISES:
            value = "Raises"
        elif _type == TokenType.RETURNS:
            value = "Returns"
        elif _type == TokenType.RPAREN:
            value = ")"
        elif _type == TokenType.WORD:
            value = random_string()
        elif _type == TokenType.YIELDS:
            value = "Yields"
        elif _type == TokenType.NOQA:
            value = "noqa"
        elif _type == TokenType.RETURN_TYPE:
            value = random_string()
        elif _type == TokenType.YIELD_TYPE:
            value = random_string()
        elif _type == TokenType.VARIABLES:
            value = random.choice(["var", "ivar", "cvar"])
        elif _type == TokenType.VARIABLE_TYPE:
            value = random_string()
        elif _type == TokenType.ARGUMENT_TYPE:
            value = random_string()
        elif _type == TokenType.OTHER:
            value = "Other"
        elif _type == TokenType.RECEIVES:
            value = "Receives"
        elif _type == TokenType.HEADER:
            value = "--------"
        elif _type == TokenType.WARNS:
            value = "Warns"
        elif _type == TokenType.SEE:
            value = "See"
        elif _type == TokenType.ALSO:
            value = "Also"
        elif _type == TokenType.NOTES:
            value = "Notes"
        elif _type == TokenType.EXAMPLES:
            value = "Examples"
        elif _type == TokenType.REFERENCES:
            value = "References"
        else:
            raise Exception("Unexpected token type {}".format(_type))
        ret.append(
            Token(
                token_type=_type,
                value=value,
                line_number=line_number,
            )
        )
        line_number += random.choice([0, 1])
    return ret


def reindent(program):
    """Reindent the program.

    This makes it a little more natural for writing the
    program in a string.

    Args:
        program: A program which is indented too much.

    Returns:
        The program, reindented.

    """

    # Find the first non-space character in a line.
    def _non_space(line):
        for i, c in enumerate(line):
            if c != " ":
                return i
        return -1

    lines = program.split("\n")
    amount = min(filter(lambda x: x >= 0, map(_non_space, lines)))
    ret = "\n".join(line[amount:] for line in lines)
    return ret
