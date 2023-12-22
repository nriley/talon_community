from talon import Context, Module, actions

ctx = Context()
mod = Module()

ctx.matches = r"""
app: excel_win
"""


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.key("alt-w n")
