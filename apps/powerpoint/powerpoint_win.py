from talon import Context, actions

ctx = Context()
ctx.matches = r"""
app: powerpoint_win
"""


def focus_slides():
    actions.key("f6:2 esc")


@ctx.action_class("user")
class UserActions:
    def copy_style():
        actions.key("ctrl-shift-c")

    def paste_style():
        actions.key("ctrl-shift-v")

    # user.pages
    def page_next():
        focus_slides()
        actions.key("pagedown")

    def page_previous():
        focus_slides()
        actions.key("pageup")

    def page_final():
        focus_slides()
        actions.key("end")
