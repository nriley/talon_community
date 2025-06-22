from talon import Context, Module, actions, app, ctrl, ui

mod = Module()
mod.tag("meeting_webex", desc="Tag to indicate that the user is in a Webex meeting")

ctx = Context()
ctx.matches = r"""
tag: user.meeting_webex
os: mac
"""

WEBEX_BUNDLE_ID = "Cisco-Systems.Spark"


def is_webex(app):
    return app.bundle == WEBEX_BUNDLE_ID


def webex_app():
    if apps := ui.apps(bundle=WEBEX_BUNDLE_ID):
        return apps[0]
    return None


def webex_window_is_meeting_window(window):
    return window.element.get("AXIdentifier") in (
        "PopOutWindow",
        "FloatingMediaWindow",
    )


def webex_window():
    if webex := webex_app():
        for window in webex.windows():
            if webex_window_is_meeting_window(window):
                return window
    return None


def is_webex_meeting_window(window):
    return is_webex(window.app) and webex_window_is_meeting_window(window)


def webex_toggle_mute():
    if webex := webex_app():
        ctrl.key_press("m", super=True, shift=True, app=webex)


def on_win_open(window):
    if is_webex_meeting_window(window):
        actions.user.meeting_started("webex", window)
        ui.register("win_focus", on_win_focus)


def on_win_focus(window):
    if is_webex_meeting_window(window):
        return

    if webex_window():
        return

    actions.user.meeting_ended("webex", window)
    ui.unregister("win_focus", on_win_focus)


def on_ready():
    if meeting_window := webex_window():
        actions.user.meeting_started("webex", meeting_window)
        ui.register("win_focus", on_win_focus)

    ui.register("win_open", on_win_open)


@ctx.action_class("user")
class UserActions:
    def meeting_is_muted() -> bool:
        if webex := webex_app():
            try:
                mute_menu_item = webex.element.children.find_one(
                    AXRole="AXMenuBar", max_depth=0
                ).children.find_one(
                    AXRole="AXMenuItem", AXMenuItemCmdChar="M", AXMenuItemCmdModifiers=1
                )
                return not mute_menu_item.AXEnabled
            except ui.UIErr:
                pass

        app.notify(
            title="Webex",
            body="Can’t determine whether Webex is muted. Is the meeting started?",
        )
        return False

    def meeting_mute():
        if actions.user.meeting_is_muted():
            return
        webex_toggle_mute()

    def meeting_unmute():
        if not actions.user.meeting_is_muted():
            return
        webex_toggle_mute()

    def meeting_exit():
        if webex := webex_app():
            webex.quit()


app.register("ready", on_ready)
