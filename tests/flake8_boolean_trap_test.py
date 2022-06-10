import ast
import json
from pathlib import Path

from flake8_boolean_trap import Plugin
from flake8_boolean_trap import BooleanTrapReason


code = (Path(__file__).parent / "checkme.py").read_text()


EXPECTED = {
    4: BooleanTrapReason.TYPE_HINT.value.format(arg="posonly_boolhint", func="function"),
    5: BooleanTrapReason.TYPE_HINT.value.format(arg="posonly_boolstrhint", func="function"),
    10: BooleanTrapReason.TYPE_HINT.value.format(arg="posorkw_nonvalued_boolhint", func="function"),
    11: BooleanTrapReason.TYPE_HINT.value.format(arg="posorkw_nonvalued_boolstrhint", func="function"),
    12: BooleanTrapReason.DEFAULT_VALUE.value.format(arg="posorkw_boolvalued_nohint", func="function"),
    13: BooleanTrapReason.DEFAULT_VALUE.value.format(arg="posorkw_boolvalued_nonboolhint", func="function"),
    14: BooleanTrapReason.TYPE_HINT.value.format(arg="posorkw_boolvalued_boolhint", func="function"),
    14: BooleanTrapReason.DEFAULT_VALUE.value.format(arg="posorkw_boolvalued_boolhint", func="function"),
    15: BooleanTrapReason.TYPE_HINT.value.format(arg="posorkw_boolvalued_boolstrhint", func="function"),
    15: BooleanTrapReason.DEFAULT_VALUE.value.format(arg="posorkw_boolvalued_boolstrhint", func="function"),
    18: BooleanTrapReason.TYPE_HINT.value.format(arg="posorkw_nonboolvalued_boolhint", func="function"),
    19: BooleanTrapReason.TYPE_HINT.value.format(arg="posorkw_nonboolvalued_boolstrhint", func="function"),
}


def dict_compare(incoming, reference):
    d1_keys = set(incoming.keys())
    d2_keys = set(reference.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (incoming[o], reference[o]) for o in shared_keys if incoming[o] != reference[o]}
    same = set(o for o in shared_keys if incoming[o] == reference[o])
    return added, removed, modified, same

def results(s):
    return {
        r[0]: r[2]
        for r in Plugin(ast.parse(s)).run()
    }


def test_normal_assignment_ok():
    received = results(code)
    added, removed, modified, _ = dict_compare(received, EXPECTED)
    assert not added, f"false positives found: {[(k,received[k]) for k in added]}"
    assert not removed, f"false negatives (missing): {[(k,EXPECTED[k]) for k in removed]}"
    assert not modified, f"boolean trap misdetection: {[(k,received[k]) for k in modified]}"
