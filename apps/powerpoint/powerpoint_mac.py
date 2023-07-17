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
