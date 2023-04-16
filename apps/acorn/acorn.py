from talon import Context, Module, actions

mod = Module()
mod.apps.acorn = """
os: mac
and app.bundle: com.flyingmeat.Acorn7
"""

ctx = Context()
ctx.matches = r"""
app: acorn
"""


@ctx.action_class("edit")
class EditActions:
    def zoom_reset():
        actions.key("cmd-1")


@ctx.action_class("user")
class UserActions:
    def zoom_to_fit():
        actions.key("cmd-0")
