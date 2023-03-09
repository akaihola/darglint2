import ast
from typing import Any, Dict, List


class VariableVisitor(ast.NodeVisitor):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # TODO: https://github.com/python/mypy/issues/4001
        super(VariableVisitor, self).__init__(*args, **kwargs)  # type: ignore
        self.variables: List[ast.Name] = list()

    def visit_Name(self, node: ast.Name) -> ast.AST:
        # Only gather names during assignment.  Others are unnecessary,
        # and could be from a different context.
        if hasattr(node, "ctx") and isinstance(node.ctx, ast.Store):
            self.variables.append(node)
        return self.generic_visit(node)
