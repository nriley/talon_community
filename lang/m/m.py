from talon import Context, Module, actions

from ...core.described_functions import create_described_insert_between
from ...lang.tags.operators import Operator, Operators

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: m
"""

mod.list("code_operators_m", desc="List of code operators for M")


class MOperators(Operators):
    STRING_FOLLOWS: Operator
    STRING_NOT_FOLLOWS: Operator
    STRING_SORTS_AFTER: Operator
    STRING_NOT_SORTS_AFTER: Operator
    STRING_PATTERN_MATCH: Operator
    STRING_PATTERN_NOT_MATCH: Operator
    STRING_CONCATENATE: Operator


operators = MOperators(
    # code_operators_array
    SUBSCRIPT=create_described_insert_between("(", ")"),
    # code_operators_assignment
    ASSIGNMENT="=",
    ASSIGNMENT_INCREMENT=create_described_insert_between("$i(", ")"),
    # code_operators_math
    MATH_SUBTRACT="-",
    MATH_ADD="+",
    MATH_MULTIPLY="*",
    MATH_DIVIDE="/",
    MATH_INTEGER_DIVIDE="\\",
    MATH_MODULO="#",
    MATH_EXPONENT="**",
    MATH_EQUAL="=",
    MATH_NOT_EQUAL="'=",
    MATH_GREATER_THAN=">",
    MATH_GREATER_THAN_OR_EQUAL=">=",
    MATH_LESS_THAN="<",
    MATH_LESS_THAN_OR_EQUAL="<=",
    MATH_AND="&",
    MATH_OR="!",
    MATH_NOT="'",
    # these are actually string operators
    MATH_IN="[",
    MATH_NOT_IN="'[",
    # name, not pointer operators, but close enough
    POINTER_INDIRECTION="@",
    POINTER_ADDRESS_OF=create_described_insert_between("$na(", ")"),
    # M operators
    STRING_FOLLOWS="]",
    STRING_NOT_FOLLOWS="']",
    STRING_SORTS_AFTER="]]",
    STRING_NOT_SORTS_AFTER="']]",
    STRING_PATTERN_MATCH="?",
    STRING_PATTERN_NOT_MATCH="'?",
    STRING_CONCATENATE="_",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators():
        return operators

    def code_insert_function(text, selection):
        substitutions = {}
        if text:
            substitutions["1"] = text
        if selection:
            substitutions["0"] = selection
        actions.user.insert_snippet_by_name("functionCall", substitutions)
