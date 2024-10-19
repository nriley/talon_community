from talon import Context, actions, app, ui

ctx = Context()
ctx.matches = r"""
app: sublime_merge_win
"""


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.key("ctrl-shift-n")

    def window_close():
        actions.key("ctrl-shift-w")

    def tab_next():
        actions.key("ctrl-pagedown")

    def tab_previous():
        actions.key("ctrl-pageup")
