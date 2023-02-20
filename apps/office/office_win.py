from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.excel_win = """
os: windows
and app.exe: EXCEL.EXE
"""
mod.apps.powerpoint_win = r"""
os: windows
and app.exe: POWERPNT.EXE
"""
mod.apps.word_win = r"""
os: windows
and app.exe: WINWORD.EXE
"""
mod.apps.office_win = r"""
app: excel_win
app: powerpoint_win
app: word_win
"""

ctx.matches = """
app: office_win
"""


@ctx.action_class("user")
class UserActions:
    def office_tell_me():
        actions.key("alt-q")
