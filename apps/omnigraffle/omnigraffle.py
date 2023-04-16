from talon import Context, Module, actions

mod = Module()
mod.apps.omnigraffle = """
os: mac
and app.bundle: com.omnigroup.OmniGraffle7
"""

ctx = Context()
ctx.matches = r"""
app: omnigraffle
"""


@ctx.action_class("edit")
class EditActions:
    def zoom_in():
        actions.key("cmd-shift-.")

    def zoom_out():
        actions.key("cmd-shift-,")

    def zoom_reset():
        actions.key("cmd-alt-0")


@ctx.action_class("user")
class UserActions:
    def zoom_to_fit():
        actions.user.menu_select("View|Zoom|Fit in Window")
