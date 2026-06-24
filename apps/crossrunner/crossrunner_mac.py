from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.crossrunner = r"""
os: mac
and app.bundle: com.utmapp.UTM
"""

ctx.matches = r"""
os: mac
app: crossrunner
"""


@ctx.action_class("user")
class UserActions:
    def debugger_step_into():
        actions.key("f11")

    def debugger_step_over():
        actions.key("f10")

    def debugger_continue():
        actions.key("f5")

    def debugger_stop():
        actions.key("shift-f5")

    def debugger_break_here():
        actions.key("f9")

    def debugger_goto_address():
        actions.key("ctrl-g")
