from talon import Context, actions, ui
from talon.mac import applescript

ctx = Context()
ctx.matches = r"""
os: mac
"""


@ctx.action_class("app")
class AppActions:
    def preferences():
        actions.key("cmd-,")

    def tab_close():
        actions.key("cmd-w")

    def tab_next():
        actions.key("ctrl-tab")

    def tab_open():
        actions.key("cmd-t")

    def tab_previous():
        actions.key("ctrl-shift-tab")

    def tab_reopen():
        actions.key("cmd-shift-t")

    def window_close():
        actions.key("cmd-w")

    def window_hide():
        ui.active_app().element.AXHidden = True

    def window_hide_others():
        applescript.run(
            """
use framework "Foundation"
set NSWorkspace to current application's class "NSWorkspace"
NSWorkspace's sharedWorkspace's hideOtherApplications()
"""
        )

    def window_open():
        actions.key("cmd-n")

    def window_previous():
        actions.key("cmd-shift-`")

    def window_next():
        actions.key("cmd-`")


@ctx.action_class("user")
class UserActions:
    def switcher_focus_last():
        actions.key("cmd-tab")

    def window_minimize():
        if window := ui.active_window():
            window.minimized = 1
            return
        actions.key("cmd-m")
