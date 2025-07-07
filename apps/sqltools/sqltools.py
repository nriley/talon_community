from talon import Context, Module, actions, ui

mod = Module()
ctx = Context()

mod.apps.sqltools = """
os: windows
and app.exe: sqltoolsu.exe
"""

mod.apps.sqltools = """
app: citrix_desktop_mac
and code.language: sql
"""

ctx.matches = """
app: sqltools
"""

ctx_win = Context()
ctx_win.matches: """
os: windows
app: sqltools
"""

@ctx.action_class("code")
class CodeActions:
    def language():
        return "sql"


@ctx.action_class("edit")
class EditActions:
    def indent_more():
        actions.key("ctrl-i")

    def indent_less():
        actions.key("ctrl-u")
    
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

@mod.action_class
class Actions:
    def sqltools_select_pane(name: str):
        """Selects/focuses the specified pane in SQLTools for Oracle"""


@ctx_win.action_class("user")
class UserActions:
    def sqltools_select_pane(name):
        window = next(w for w in ui.active_app().windows() if w.title == "SQLTools")
        buttons = window.element.find(control_type="RadioButton")
        button_index, button = next((i, b) for i, b in enumerate(buttons) if b.name.startswith(name))
        if button.selectionitem_pattern.is_selected:
            other_index = button_index - 1 if button_index > 0 else 1
            buttons[other_index].invoke_pattern.invoke()
        buttons[button_index].invoke_pattern.invoke()

