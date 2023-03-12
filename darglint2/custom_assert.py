"""Defines a custom assert function for darglint2."""

from typing import Any, Optional

from .config import AssertStyle, get_config, get_logger


def Assert(expr: Any, message: Optional[str]) -> None:
    """Asserts that the given expression is true.

    Args:
        expr: The expression to evaluate.  It will be
            interpreted as a boolean.
        message: A message describing the expectation of
            this assertion, describing the error encountered,
            or some other debugging information.

    Raises:
        AssertionError: If darglint2 is configured to raise
            on failed assertions, otherwise logs.

    """
    if expr:
        return

    style = get_config().assert_style
    if style == AssertStyle.RAISE:
        raise AssertionError(message)
    elif style == AssertStyle.LOG:
        logger = get_logger()
        logger.error(message or "Failed assertion")
