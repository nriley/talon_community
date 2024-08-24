from talon import Context, Module, actions, ctrl, ui

mod = Module()

mod.apps.xcode = r"""
os: mac
and app.bundle: com.apple.dt.Xcode
"""

ctx = Context()
ctx.matches = r"""
app: xcode
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
    def find(text: str = None):
        actions.key("cmd-f")
        if text:
            actions.insert(text)

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
    def find_everywhere(text: str):
        actions.key("cmd-shift-f")
        actions.insert(text)

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

    # user.splits (partial)
    def split_window_vertically():
        actions.key("cmd-ctrl-t")

    def split_window_horizontally():
        actions.key("cmd-alt-ctrl-t")

    def split_flip():
        actions.user.menu_select("View|Change Editor Orientation")

    def split_reset():
        actions.user.menu_select("View|Reset Editor Sizes")

    split_window = split_window_vertically

    def split_clear():
        actions.key("cmd-shift-ctrl-w")

    def split_clear_all():
        actions.key("cmd-shift-alt-ctrl-w")

    def split_maximize():
        actions.key("cmd-shift-ctrl-return")

    def split_next():
        # I use this shortcut for toggling Talon, so send directly to app
        ctrl.key_press("`", ctrl=True, app=ui.active_app())

    def split_last():
        actions.key("shift-ctrl-`")


@ctx.action_class("win")
class WinActions:
    def filename():
        return actions.win.title()
