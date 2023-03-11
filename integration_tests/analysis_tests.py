import os
from unittest import TestCase
from unittest.mock import (
    patch,
    Mock,
)

import ast
from darglint2.analysis.raise_visitor import (
    RaiseVisitor,
)
from darglint2.config import (
    AssertStyle,
)
from darglint2.function_description import (
    read_program,
    get_function_descriptions,
)
from darglint2.utils import (
    ConfigurationContext,
)


def yield_modules():
    # type: () -> Iterable[str]
    for path, folders, filenames in os.walk('integration_tests/repos'):
        for filename in filenames:
            if not filename.endswith('.py'):
                continue
            yield os.path.join(path, filename)


class RaiseAnalysisTest(TestCase):

    @patch("darglint2.analysis.raise_visitor.logger")
    def test_no_errors_logged_ever(self, mock_logger):
        """Make sure that no functions kill the analysis.

        We patch the logger to make sure no error-level message
        is recorded.  An error-level message indicates that there
        is an unexpected branch we did not cover.

        """
        mock_logger.error = Mock()
        visitor = RaiseVisitor()

        # Force assert to raise an error -- this will help to
        # distinguish it from the logger errors.
        with ConfigurationContext(assert_style=AssertStyle.RAISE):
            for module in yield_modules():
                program = read_program(module)
                try:
                    tree = ast.parse(program)
                except:
                    # If it doesn't parse, then it's probably Python2,
                    # or something is invalid and we don't care.
                    # We only want to check files which are valid
                    # Python.
                    continue
                functions = get_function_descriptions(tree)
                for function in functions:
                    try:
                        visitor.visit(function.function)
                    except:
                        print('Visitor error raised during {}'.format(module))
                        raise
                    self.assertFalse(
                        mock_logger.error.called,
                        'Unexpected error log at {}'.format(
                            module,
                        )
                    )
