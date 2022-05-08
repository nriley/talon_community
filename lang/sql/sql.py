from talon import Context, actions
ctx = Context()
ctx.matches = r"""
tag: user.sql
"""

# these vary by dialect
ctx.lists["user.code_functions"] = {
    "count": "Count",
    "min": "Min",
    "max": "Max"
}

@ctx.action_class('user')
class UserActions:
    def code_operator_addition(): actions.auto_insert(' + ')
    def code_operator_subtraction(): actions.auto_insert(' - ')
    def code_operator_multiplication(): actions.auto_insert(' * ')
    def code_operator_division(): actions.auto_insert(' / ')

    def code_operator_equal(): actions.auto_insert(' = ')
    def code_operator_not_equal(): actions.auto_insert(' <> ')
    def code_operator_greater_than(): actions.auto_insert(' > ')
    def code_operator_greater_than_or_equal_to(): actions.auto_insert(' >= ')
    def code_operator_less_than(): actions.auto_insert(' < ')
    def code_operator_less_than_or_equal_to(): actions.auto_insert(' <= ')
    def code_operator_in():
        actions.auto_insert(' IN ()')
        actions.key('left')
    def code_operator_not_in():
        actions.auto_insert(' NOT IN ()')
        actions.key('left')

    def code_operator_and(): actions.auto_insert('AND ')
    def code_operator_or(): actions.auto_insert('OR ')

    def code_insert_null():        actions.auto_insert('NULL')
    def code_insert_is_null():     actions.auto_insert(' IS NULL')
    def code_insert_is_not_null(): actions.auto_insert(' IS NOT NULL')

    def code_comment_line_prefix(): actions.auto_insert('-- ')

    def code_insert_function(text: str, selection: str):
        if selection:
            text = f"{text}({selection})"
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()
