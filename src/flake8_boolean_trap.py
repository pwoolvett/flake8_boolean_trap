"""Capture and report three different conditions for boolean traps.

Currently detects three conditions:

* `BooleanTrapReason.TYPE_HINT`: positional args in function defs.
* `BooleanTrapReason.DEFAULT_VALUE`: boolean default values in function defs.
* `BooleanTrapReason.FUNCTION_CALL`: positional boolean args in function calls.

See Also:

    `BooleanTrapReason`
"""

from __future__ import annotations

import ast
from enum import Enum
from typing import List
from typing import Tuple
from typing import Type
from typing import Union

try:
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata  # type: ignore
from typing import Any
from typing import Generator


class BooleanTrapReason(Enum):
    """Defines boolean trap detection reasons.

    Enum values should contain a string template to be formatted
    """

    TYPE_HINT = (
        "FBT001 do not define boolean positional args."
        " Hint: in `def {func}(...)` , define `{arg}` as kw-only"
    )
    """Function definition contains boolean type hint in positional arg."""

    DEFAULT_VALUE = (
        "FBT002 do not set boolean defaults for positional args."
        " Hint: in `def {func}(...)`, define `{arg}` as kw-only"
    )
    """Function definition contains boolean default in positional arg."""

    FUNCTION_CALL = (
        "FBT003 do not use boolean positional args."
        " Hint: in `{func}(..)`,"
        " refactor positional arg #{position} to include its argument name"
    )
    """Function call uses boolean positional arg."""


BooleanTrapRegistry = List[Tuple[int, int, Union[str, int], str, BooleanTrapReason]]
CandidateGen = Generator[Tuple[ast.expr, int, int, str], None, None]
LintError = Tuple[int, int, str, Type[Any]]
LintErrorGen = Generator[LintError, None, None]


def positional_hints(func_node: ast.FunctionDef) -> CandidateGen:
    """Extract type hints from postiional arguments.

    Args:
        func_node: Function ast containing the arguments to search.

    Yields:
        Type annotations for arguments which could be used as positional.
    """
    for arg in func_node.args.posonlyargs + func_node.args.args:
        hint = arg.annotation
        if hint is not None:
            yield hint, arg.lineno, arg.col_offset, arg.arg


def is_boolean_typehint(hint: ast.expr) -> bool:
    """Detect whether a type hint corresponds to a boolean.

    Args:
        hint: Type hint ast.

    Returns:
        True if the type hint corresponds to a boolean
    """

    return any(
        (
            isinstance(hint, ast.Name) and hint.id == "bool",
            isinstance(hint, ast.Constant) and hint.value == "bool",
        )
    )


def default_values(func_node: ast.FunctionDef) -> CandidateGen:
    """Retrieve function args and respective default values.

    Args:
        func_node: The functions ast to parse its args. Args are
            iterated in reversed order because sizes could differ.

    "defaults is a list of default values for arguments that can be
    passed positionally. If there are fewer defaults, they correspond to
    the last n arguments."

    Yields:
        Candidates for args with default values.

    See Also:
        https://docs.python.org/3/library/ast.html#ast.arguments

    """

    arg_defaults = zip(reversed(func_node.args.args), reversed(func_node.args.defaults))
    for arg, default in arg_defaults:
        yield default, default.lineno, default.col_offset, arg.arg


def is_boolean_default(default: ast.expr) -> bool:
    """Detect whether a default argument value is a boolean.

    Args:
        default: Default parameter value ast.

    Returns:
        True if the default value is a boolean
    """
    return isinstance(default, ast.Constant) and isinstance(default.value, bool)


class Visitor(ast.NodeVisitor):
    """Ast visitor to group violations in a registry.

    Currently visits only function definitions and calls, where boolean
    traps might be located. See `Visitor.visit_FunctionDef` and
    `Visitor.visit_Call`, respectively.
    """

    def __init__(self) -> None:
        """Initialize the node visitor with an empty registry."""
        self.registry: BooleanTrapRegistry = []

    def visit_FunctionDef(self, func_node: ast.FunctionDef) -> None:  # noqa: N802
        """Capture boolean traps in function definitions.

        Args:
            func_node: the function ast to inspect.

        See Also
            * `BooleanTrapReason.TYPE_HINT`: `positional_hints`, `is_boolean_typehint`
            * `BooleanTrapReason.DEFAULT_VALUE`: `default_values`, `is_boolean_default`

        """
        for hint, lineno, col, argname in positional_hints(func_node):
            if is_boolean_typehint(hint):
                self.registry.append(
                    (lineno, col, argname, func_node.name, BooleanTrapReason.TYPE_HINT)
                )

        for default, lineno, col, argname in default_values(func_node):
            if is_boolean_default(default):
                self.registry.append(
                    (
                        lineno,
                        col,
                        argname,
                        func_node.name,
                        BooleanTrapReason.DEFAULT_VALUE,
                    )
                )

        self.generic_visit(func_node)

    def visit_Call(self, call: ast.Call) -> None:  # noqa: N802
        """Capture boolean traps in function calls.

        Args:
            call: the call ast to inspect.

        See Also
            `BooleanTrapReason.FUNCTION_CALL`

        """

        for position, arg in enumerate(call.args):
            if (
                isinstance(arg, ast.Constant)
                and isinstance(arg.value, bool)
                and isinstance(call.func, ast.Name)
            ):
                self.registry.append(
                    (
                        call.lineno,
                        call.col_offset,
                        position,
                        call.func.id,
                        BooleanTrapReason.FUNCTION_CALL,
                    )
                )

        self.generic_visit(call)


class Plugin:  # noqa: R0903
    """Flake8 plugin implementation.

    Just reports the violations stored in `Visitor.registry`
    """

    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST) -> None:
        """Initialize flake8 plugin by storing the ast tree at instance level.

        Args:
            tree: the whole module ast tree to parse.
        """
        self._tree = tree

    def run(self) -> LintErrorGen:
        """Report lint errors as parsed from `Visitor`.

        Yields:
            Boolean trap detections with their location and reason.
        """
        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col, arg_or_pos, func, reason in visitor.registry:
            if reason == BooleanTrapReason.FUNCTION_CALL:
                yield line, col, reason.value.format(
                    position=arg_or_pos, func=func
                ), type(self)
            else:
                yield line, col, reason.value.format(arg=arg_or_pos, func=func), type(
                    self
                )
