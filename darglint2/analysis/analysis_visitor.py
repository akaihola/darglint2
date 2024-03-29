from .abstract_callable_visitor import AbstractCallableVisitor
from .argument_visitor import ArgumentVisitor
from .assert_visitor import AssertVisitor
from .function_scoped_visitor import FunctionScopedVisitorMixin
from .raise_visitor import RaiseVisitor
from .return_visitor import ReturnVisitor
from .variable_visitor import VariableVisitor
from .yield_visitor import YieldVisitor


# ATTENTION: FunctionScopedVisitorMixin needs to be first,
# otherwise it is not able to stop descending into wrapped
# functions.
class AnalysisVisitor(
    FunctionScopedVisitorMixin,
    AbstractCallableVisitor,
    RaiseVisitor,
    YieldVisitor,
    ArgumentVisitor,
    VariableVisitor,
    ReturnVisitor,
    AssertVisitor,
):
    """Finds attributes which should be part of the function signature."""

    pass
