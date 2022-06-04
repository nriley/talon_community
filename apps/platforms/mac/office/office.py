from talon import Context, Module, ui

mod = Module()
ctx = Context()

mod.apps.excel_mac = """
os: mac
and app.bundle: com.microsoft.Excel
"""
mod.apps.powerpoint_mac = r"""
os: mac
and app.bundle: com.microsoft.Powerpoint
"""
mod.apps.word_mac = r"""
os: mac
and app.bundle: com.microsoft.Word
"""
mod.apps.office_mac = r"""
app: excel_mac
app: powerpoint_mac
app: word_mac
"""

ctx.matches = """
app: office_mac
"""


def document_window():
    return ui.active_app().children.find_one(
        AXRole="AXWindow", AXSubrole="AXStandardWindow", max_depth=0
    )


@ctx.action_class("user")
class UserActions:
    def office_tell_me():
        (
            document_window()
            .children.find_one(AXRole="AXTabGroup", max_depth=0)
            .children.find_one(AXRole="AXButton", max_depth=0)
        ).perform("AXPress")


@mod.action_class
class Actions:
    def office_tell_me():
        """Focus 'Tell me' in Microsoft Office apps"""
