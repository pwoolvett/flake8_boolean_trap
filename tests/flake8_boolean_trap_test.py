from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path
from typing import Dict
from typing import Set

from flake8_boolean_trap import BooleanTrapReason
from flake8_boolean_trap import Plugin

RegistryPerLine = Dict[int, Set[str]]

EXPECTED: RegistryPerLine = {
    4: {
        BooleanTrapReason.TYPE_HINT.value.format(
            arg="posonly_boolhint", func="function"
        )
    },
    5: {
        BooleanTrapReason.TYPE_HINT.value.format(
            arg="posonly_boolstrhint", func="function"
        )
    },
    10: {
        BooleanTrapReason.TYPE_HINT.value.format(
            arg="posorkw_nonvalued_boolhint", func="function"
        )
    },
    11: {
        BooleanTrapReason.TYPE_HINT.value.format(
            arg="posorkw_nonvalued_boolstrhint", func="function"
        )
    },
    12: {
        BooleanTrapReason.DEFAULT_VALUE.value.format(
            arg="posorkw_boolvalued_nohint", func="function"
        )
    },
    13: {
        BooleanTrapReason.DEFAULT_VALUE.value.format(
            arg="posorkw_boolvalued_nonboolhint", func="function"
        )
    },
    14: {
        BooleanTrapReason.TYPE_HINT.value.format(
            arg="posorkw_boolvalued_boolhint", func="function"
        ),
        BooleanTrapReason.DEFAULT_VALUE.value.format(
            arg="posorkw_boolvalued_boolhint", func="function"
        ),
    },
    15: {
        BooleanTrapReason.TYPE_HINT.value.format(
            arg="posorkw_boolvalued_boolstrhint", func="function"
        ),
        BooleanTrapReason.DEFAULT_VALUE.value.format(
            arg="posorkw_boolvalued_boolstrhint", func="function"
        ),
    },
    18: {
        BooleanTrapReason.TYPE_HINT.value.format(
            arg="posorkw_nonboolvalued_boolhint", func="function"
        )
    },
    19: {
        BooleanTrapReason.TYPE_HINT.value.format(
            arg="posorkw_nonboolvalued_boolstrhint", func="function"
        )
    },
    43: {
        BooleanTrapReason.FUNCTION_CALL.value.format(position=0, func="used"),
    },
}


def get_misdetections(*, reference: RegistryPerLine, incoming: RegistryPerLine, key):
    if key not in incoming:
        errors = [f"False Negative for `{key}`: `{msg}`" for msg in reference[key]]
    elif key not in reference:
        errors = [f"False Positive for `{key}`: `{msg}`" for msg in incoming[key]]
    else:
        errors = [
            *[
                f"False Negative for `{key}`: `{msg}`"
                for msg in reference[key]
                if msg not in incoming[key]
            ],
            *[
                f"False Positive for `{key}`: `{msg}`"
                for msg in incoming[key]
                if msg not in reference[key]
            ],
        ]
    return errors


def lint_once() -> RegistryPerLine:

    checkme = (Path(__file__).parent / "checkme.py").read_text()

    registry = defaultdict(set)
    for r in Plugin(ast.parse(checkme)).run():
        registry[r[0]].add(r[2])

    return registry


def pytest_generate_tests(
    metafunc,
):
    if "key_from_union" in metafunc.fixturenames:
        lint_result = lint_once()
        all_keys = set(EXPECTED.keys()).union(set(lint_result.keys()))
        metafunc.parametrize("key_from_union", all_keys)
        metafunc.parametrize("lint_result", [lint_result])


def test_boolean_trap(key_from_union, lint_result):
    errors = get_misdetections(
        reference=EXPECTED, incoming=lint_result, key=key_from_union
    )
    assert not errors, "\t".join(errors)
