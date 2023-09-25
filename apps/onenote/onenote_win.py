from talon import Context, Module, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
app: onenote_win
"""

@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.user.office_win_ribbon_select("wn")


@ctx.action_class("edit")
class EditActions:
    def select_line(n: int = None):
        actions.key("ctrl-a")

    def zoom_in():
        actions.key("ctrl-alt-shift-+")

    def zoom_out():
        actions.key("ctrl-alt-shift--")

    def zoom_reset():
        actions.user.office_win_ribbon_select("w1")


@ctx.action_class("user")
class UserActions:
    def onenote_font_size(size):
        actions.user.office_win_ribbon_select("hfs")
        if size:
            actions.sleep("20ms")
            actions.insert(f"{size}")
            actions.key("enter esc")

    def zoom_to_fit_width():
        actions.user.office_win_ribbon_select("wi")
