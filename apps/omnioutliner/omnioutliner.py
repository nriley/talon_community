from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.omnioutliner = r"""
os: mac
and app.bundle: com.omnigroup.OmniOutliner6
"""

ctx.matches = r"""
os: mac
app: omnioutliner
"""


@ctx.action_class("edit")
class EditActions:
    def zoom_in():
        actions.key("cmd-shift-.")

    def zoom_out():
        actions.key("cmd-shift-,")

    def zoom_reset():
        actions.user.menu_select("View|Zoom to Actual Size")
