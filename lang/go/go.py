from talon import Context, Module, actions, settings

mod = Module()

ctx = Context()
ctx.matches = r"""
tag: user.go
"""

ctx.lists["user.code_type"] = {
    "you int eight": "uint8",
    "you int sixteen": "uint16",
    "you int thirty two": "uint32",
    "you int sixty four": "uint64",
    "int eight": "int8",
    "int sixteen": "int16",
    "int thirty two": "int32",
    "int sixty four": "int64",
    "float thirty two": "float32",
    "float sixty four": "float64",
    "complex sixty four": "complex64",
    "complex one twenty eight": "complex128",
    "byte": "byte",
    "rune": "rune",
    "you int": "uint",
    "int": "int",
    "you int pointer": "uintptr",
}


@ctx.action_class("user")
class UserActions:
    def code_operator_indirection():
        actions.auto_insert("*")

    def code_operator_address_of():
        actions.auto_insert("&")

    def code_operator_structure_dereference():
        actions.auto_insert(".")

    def code_operator_subscript():
        actions.insert("[]")
        actions.key("left")

    def code_operator_assignment():
        actions.auto_insert(" = ")

    def code_operator_subtraction():
        actions.auto_insert(" - ")

    def code_operator_subtraction_assignment():
        actions.auto_insert(" -= ")

    def code_operator_addition():
        actions.auto_insert(" + ")

    def code_operator_addition_assignment():
        actions.auto_insert(" += ")

    def code_operator_multiplication():
        actions.auto_insert(" * ")

    def code_operator_multiplication_assignment():
        actions.auto_insert(" *= ")

    # action(user.code_operator_exponent): " ** "
    def code_operator_division():
        actions.auto_insert(" / ")

    def code_operator_division_assignment():
        actions.auto_insert(" /= ")

    def code_operator_modulo():
        actions.auto_insert(" % ")

    def code_operator_modulo_assignment():
        actions.auto_insert(" %= ")

    def code_operator_equal():
        actions.auto_insert(" == ")

    def code_operator_not_equal():
        actions.auto_insert(" != ")

    def code_operator_greater_than():
        actions.auto_insert(" > ")

    def code_operator_greater_than_or_equal_to():
        actions.auto_insert(" >= ")

    def code_operator_less_than():
        actions.auto_insert(" < ")

    def code_operator_less_than_or_equal_to():
        actions.auto_insert(" <= ")

    def code_operator_and():
        actions.auto_insert(" && ")

    def code_operator_or():
        actions.auto_insert(" || ")

    def code_operator_bitwise_and():
        actions.auto_insert(" & ")

    def code_operator_bitwise_and_assignment():
        actions.auto_insert(" &= ")

    def code_operator_bitwise_or():
        actions.auto_insert(" | ")

    def code_operator_bitwise_or_assignment():
        actions.auto_insert(" |= ")

    def code_operator_bitwise_exclusive_or():
        actions.auto_insert(" ^ ")

    def code_operator_bitwise_exclusive_or_assignment():
        actions.auto_insert(" ^= ")

    def code_operator_bitwise_left_shift():
        actions.auto_insert(" << ")

    def code_operator_bitwise_left_shift_assignment():
        actions.auto_insert(" <<= ")

    def code_operator_bitwise_right_shift():
        actions.auto_insert(" >> ")

    def code_operator_bitwise_right_shift_assignment():
        actions.auto_insert(" >>= ")

    def code_insert_null():
        actions.auto_insert("nil")

    def code_insert_is_null():
        actions.auto_insert(" == nil")

    def code_insert_is_not_null():
        actions.auto_insert(" != nil")

    def code_state_if():
        actions.insert("if  {\n}\n")
        actions.key("up:2 left:3")

    def code_state_else_if():
        actions.insert("else if () {\n}\n")
        actions.key("up:2 left:3")

    def code_state_else():
        actions.insert("else\n{\n}\n")
        actions.key("up:2")

    def code_state_switch():
        actions.insert("switch  {")
        actions.key("left:2")

    def code_state_case():
        actions.insert("case :")
        actions.edit.left()

    def code_state_for():
        actions.auto_insert("for  {")
        actions.key("left:3")

    code_state_while = code_state_for

    def code_state_for_each():
        actions.auto_insert("for  := range  {")
        actions.key("left:12")

    def code_state_return():
        actions.auto_insert("return ")

    def code_break():
        actions.auto_insert("break")

    def code_next():
        actions.auto_insert("continue")

    def code_insert_true():
        actions.auto_insert("true")

    def code_insert_false():
        actions.auto_insert("false")

    def code_comment_line_prefix():
        actions.auto_insert("//")

    def code_insert_type_annotation(type: str):
        actions.insert(f" {type}")

    code_insert_return_type = code_insert_type_annotation

    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + f"({selection})"
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()

    def code_private_function(text: str):
        result = "func {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )
        actions.user.code_insert_function(result, None)

    # def code_private_static_function(text: str):
    #     """Inserts private static function"""
    #     result = "static void {}".format(
    #         actions.user.formatted_text(
    #             text, settings.get("user.code_private_function_formatter")
    #         )
    #     )

    #     actions.user.code_insert_function(result, None)

    def code_insert_library(text: str, selection: str):
        actions.user.paste(f'import "{selection}"')
