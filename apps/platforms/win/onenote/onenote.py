from talon import Context, actions
ctx = Context()
ctx.matches = r"""
os: windows
and app.exe: ONENOTE.EXE
"""

@ctx.action_class('edit')
class EditActions:
    def select_line(n: int=None):
        actions.key('ctrl-a')

@ctx.action_class('user')
class UserActions:
    def onenote_font_size(size):
        actions.key("alt-h")
        actions.sleep("50ms")
        actions.key("f s")
        if size:
            actions.sleep("50ms")
            actions.insert(f"{size}")
            actions.key("enter esc")
