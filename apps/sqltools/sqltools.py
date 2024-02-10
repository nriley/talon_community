from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.sqltools = """
os: windows
and app.exe: sqltoolsu.exe
os: mac
and app: citrix_desktop
and code.language: sql
"""

ctx.matches = """
app: sqltools
"""


@ctx.action_class("code")
class CodeActions:
    def language():
        return "sql"


@ctx.action_class("edit")
class EditActions:
    # more direct word/line processing - actions are in core,
    # but voice commands are enabled with tag(user.line_commands)
    def delete_line():
        actions.key("ctrl-y")

    def line_clone():
        actions.key("esc ctrl-k q")

    def select_word():
        actions.key("ctrl-w")

    def select_line(n: int = None):
        actions.key("ctrl-l")

    def jump_line(n: int):
        actions.key("ctrl-g")
        actions.insert(str(n))
        actions.key("enter")
