import ast
from typing import Any, List, Optional


class ReturnVisitor(ast.NodeVisitor):
    """A visitor which checks for *returns* nodes."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # TODO: https://github.com/python/mypy/issues/4001
        super(ReturnVisitor, self).__init__(*args, **kwargs)  # type: ignore

        # A list of the return nodes encountered.
        self.returns: List[Optional[ast.Return]] = list()
        self.return_types: List[Optional[ast.AST]] = list()

    def visit_Return(self, node: ast.Return) -> ast.AST:
        self.returns.append(node)
        return self.generic_visit(node)
