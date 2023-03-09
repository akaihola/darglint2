import ast
from typing import Any, List, Union


class YieldVisitor(ast.NodeVisitor):
    """A visitor which checks for *returns* nodes."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # TODO: https://github.com/python/mypy/issues/4001
        super(YieldVisitor, self).__init__(*args, **kwargs)  # type: ignore

        # A list of the return nodes encountered.
        self.yields: List[Union[ast.Yield, ast.YieldFrom]] = list()

    def visit_Yield(self, node: ast.Yield) -> ast.AST:
        self.yields.append(node)
        return self.generic_visit(node)

    def visit_YieldFrom(self, node: ast.YieldFrom) -> ast.AST:
        self.yields.append(node)
        return self.generic_visit(node)
