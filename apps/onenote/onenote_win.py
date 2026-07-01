from talon import Context, Module, actions, app

mod = Module()
ctx = Context()

ctx.matches = r"""
os: windows
app: onenote_win
"""


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.user.office_ribbon_select("wn")


@ctx.action_class("edit")
class EditActions:
    def select_line(n=None):
        if n is not None:
            raise ValueError("Unable to select a specific line")
        actions.key("ctrl-a")

    def zoom_in():
        actions.key("ctrl-alt-shift-+")

    def zoom_out():
        actions.key("ctrl-alt-shift--")

    def zoom_reset():
        actions.user.office_ribbon_select("w1")


@ctx.action_class("user")
class UserActions:
    def normal_style():
        actions.key("ctrl-shift-n")

    def get_font_size():
        actions.user.office_ribbon_select("hfs")
        font_size = actions.edit.selected_text()

        if not str.isnumeric(font_size):
            app.notify(body="Unable to determine current font size", title="OneNote")
            raise RuntimeError("Can't get font size")

        return float(font_size)

    def set_font_size(size=0):
        actions.user.office_ribbon_select("hfs")
        if size:
            actions.sleep("20ms")
            actions.insert(f"{size}")
            actions.key("enter esc")

    def adjust_font_size(offset):
        if offset > 0:
            actions.key(f"ctrl-shift->:{offset}")
        else:
            actions.key(f"ctrl-shift-<:{-offset}")

    def onenote_go_progress():
        actions.key("ctrl-g home enter tab:3 home enter esc")

    def zoom_to_fit_width():
        actions.user.office_ribbon_select("wi")
