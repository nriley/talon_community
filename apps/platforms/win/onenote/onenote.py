from talon import Module, Context, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
os: windows
and app.exe: ONENOTE.EXE
"""

@ctx.action_class('edit')
class EditActions:
    def select_line(n: int=None):
        actions.key('ctrl-a')

@mod.action_class
class Actions:
    def onenote_ribbon_select(keys: str):
        """Select from the ribbon on OneNote for Windows."""

@ctx.action_class('user')
class UserActions:
    def onenote_font_size(size):
        actions.user.onenote_ribbon_select('hfs')
        if size:
            actions.sleep("20ms")
            actions.insert(f"{size}")
            actions.key("enter esc")

    def onenote_ribbon_select(keys):
        actions.key("alt-" + keys[0])
        actions.sleep("20ms")
        actions.key(' '.join(keys[1:]))
