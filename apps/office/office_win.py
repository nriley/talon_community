from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.excel_win = """
os: windows
and app.exe: excel.exe
"""
mod.apps.powerpoint_win = r"""
os: windows
and app.exe: powerpnt.exe
"""
mod.apps.word_win = r"""
os: windows
and app.exe: winword.exe
"""
mod.apps.onenote_win = r"""
os: windows
and app.exe: onenote.exe
"""
mod.apps.office_win = r"""
app: excel_win
app: powerpoint_win
app: word_win
app: onenote_win
"""

ctx.matches = """
app: office_win
"""


@mod.action_class
class Actions:
    def office_win_ribbon_select(keys: str):
        """Select from the ribbon in a Windows Office app"""


@ctx.action_class("edit")
class EditActions:
    def paste_match_style():
        actions.user.office_win_ribbon_select("hvt")


@ctx.action_class("user")
class UserActions:
    def office_tell_me():
        actions.key("alt-q")
        actions.sleep("200ms")

    def office_win_ribbon_select(keys):
        actions.key("alt-" + keys[0])
        actions.sleep("30ms")
        actions.key(" ".join(keys[1:]))
