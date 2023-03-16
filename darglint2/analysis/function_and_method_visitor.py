import ast
from typing import List, Set, Union

from .analysis_helpers import _has_decorator


class FunctionAndMethodVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.callables: Set[Union[ast.FunctionDef, ast.AsyncFunctionDef]] = set()
        self._methods: Set[Union[ast.FunctionDef, ast.AsyncFunctionDef]] = set()
        self._properties: Set[Union[ast.FunctionDef, ast.AsyncFunctionDef]] = set()

    @property
    def functions(self) -> List[Union[ast.FunctionDef, ast.AsyncFunctionDef]]:
        return list(self.callables - self._methods - self._properties)

    @property
    def methods(self) -> List[Union[ast.FunctionDef, ast.AsyncFunctionDef]]:
        return list(self._methods)

    @property
    def properties(self) -> List[Union[ast.FunctionDef, ast.AsyncFunctionDef]]:
        return list(self._properties)

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.AST:
        for item in node.body:
            if isinstance(item, ast.FunctionDef) or isinstance(
                item, ast.AsyncFunctionDef
            ):
                if _has_decorator(item, "property"):
                    self._properties.add(item)
                else:
                    self._methods.add(item)
        return self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        self.callables.add(node)
        return self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:
        self.callables.add(node)
        return self.generic_visit(node)
