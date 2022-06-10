import ast
from enum import Enum

try:
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata
from typing import Any
from typing import Generator



class BooleanTrapReason(Enum):
    TYPE_HINT = "FBT001 do not use boolean positional args. Hint: set `{arg}` as kw-only in `{func}`"
    DEFAULT_VALUE = "FBT002 do not use boolean defaults for positional args. Hint: set `{arg}` as kw-only in `{func}`"


AssignExprs = list[tuple[int, int, str, str, BooleanTrapReason]]


def positional_hints(func_node: ast.FunctionDef):
    for arg in func_node.args.posonlyargs + func_node.args.args:
        hint = arg.annotation
        if hint is not None:
            yield hint, arg.lineno, arg.col_offset, arg.arg


def is_boolean_typehint(hint) -> bool:
    return any(
        (
            isinstance(hint, ast.Name) and hint.id == "bool",
            isinstance(hint, ast.Constant) and hint.value == "bool",
        )
    )


def default_values(func_node: ast.FunctionDef):
    """Function args and respective default values.

    Iterated in reversed order because sizes could differ.

    "defaults is a list of default values for arguments that can be
    passed positionally. If there are fewer defaults, they correspond to
    the last n arguments."

    See Also:

    https://docs.python.org/3/library/ast.html#ast.arguments

    """

    arg_defaults = zip(reversed(func_node.args.args), reversed(func_node.args.defaults))
    for arg, default in arg_defaults:
        yield default, default.lineno, default.col_offset, arg.arg


def is_boolean_default(default) -> bool:
    return isinstance(default, ast.Constant) and isinstance(default.value, bool)


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.assign_exprs: AssignExprs = []

    def visit_FunctionDef(self, func_node: ast.FunctionDef) -> None:
        for hint, lineno, col, argname in positional_hints(func_node):
            if is_boolean_typehint(hint):
                self.assign_exprs.append(
                    (lineno, col, argname, func_node.name, BooleanTrapReason.TYPE_HINT)
                )

        for default, lineno, col, argname in default_values(func_node):
            if is_boolean_default(default):
                self.assign_exprs.append(
                    (
                        lineno,
                        col,
                        argname,
                        func_node.name,
                        BooleanTrapReason.DEFAULT_VALUE,
                    )
                )

        self.generic_visit(func_node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col, arg, func, reason in visitor.assign_exprs:
            yield line, col, reason.value.format(arg=arg, func=func), type(self)
