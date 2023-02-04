from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
and app.bundle: com.apple.dt.Xcode
"""


@ctx.action_class("app")
class AppActions:
    # user.tabs
    def tab_previous():
        actions.key("cmd-shift-[")

    def tab_next():
        actions.key("cmd-shift-]")

    def window_close():
        actions.key("cmd-shift-w")


@ctx.action_class("code")
class CodeActions:
    def toggle_comment():
        actions.key("cmd-/")


@ctx.action_class("edit")
class EditActions:
    def jump_line(n: int):
        actions.key("cmd-l")
        actions.insert(str(n))
        actions.key("enter")

    def indent_less():
        actions.key("cmd-[")

    def indent_more():
        actions.key("cmd-]")


@ctx.action_class("user")
class UserActions:
    # user.find_and_replace
    def find(text: str):
        actions.key("cmd-f")
        actions.insert(text)

    def find_everywhere(text: str):
        actions.key("cmd-shift-f")
        actions.insert(text)

    def find_next():
        actions.key("cmd-g")

    def find_previous():
        actions.key("cmd-shift-g")

    def replace(text: str):
        actions.key("cmd-alt-f")
        actions.insert(text)

    replace_everywhere = find_everywhere

    # user.line_commands
    def delete_camel_left():
        actions.key("ctrl-backspace")

    def delete_camel_right():
        actions.key("ctrl-delete")

    def extend_camel_left():
        actions.key("ctrl-shift-left")

    def extend_camel_right():
        actions.key("ctrl-shift-right")

    def camel_left():
        actions.key("ctrl-left")

    def camel_right():
        actions.key("ctrl-right")


@ctx.action_class("win")
class WinActions:
    def filename():
        return actions.win.title()
