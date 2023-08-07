from talon import Context, Module, actions

ctx = Context()
mod = Module()

ctx.matches = r"""
app: powerpoint_mac
"""


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.user.menu_select("Window|New Window")


@ctx.action_class("user")
class UserActions:
    def zoom_to_fit():
        actions.key("cmd-alt-o")
