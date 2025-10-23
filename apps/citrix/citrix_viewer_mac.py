from talon import Context, Module, actions, app, clip, ui

ctx = Context()
mod = Module()

mod.apps.citrix_viewer_mac = """
os: mac
and app.bundle: com.citrix.receiver.icaviewer.mac
"""

ctx.matches = """
app: citrix_viewer_mac
"""


def citrix_view_menu():
    citrix_viewer = ui.active_app()
    if citrix_viewer.bundle != "com.citrix.receiver.icaviewer.mac":
        print("Citrix Viewer is not the active application")
        return None
    menu_bar = citrix_viewer.children.find_one(AXRole="AXMenuBar", max_depth=0)
    view_menu = menu_bar.children.find_one(
        AXRole="AXMenuBarItem", AXTitle="View", max_depth=0
    ).children[0]
    return view_menu


@ctx.action_class("user")
class UserActions:
    def window_toggle_full_screen():
        view_menu = citrix_view_menu()
        menu_items = view_menu.children.find(AXRole="AXMenuItem", max_depth=0)

        if full_screen_item := next(
            (
                item
                for item in menu_items
                if item.AXTitle in ("Enter Full Screen", "Exit Full Screen")
            ),
            None,
        ):
            full_screen_item.perform("AXPress")
        else:
            app.notify(
                "Unable to find full screen menu item (non-English localization?)",
                title="Citrix Viewer",
            )

    def windows_key(key):
        if "win-" in key or "super-" in key:
            raise Exception(
                "Unable to synthesize Windows key combinations on macOS Citrix Viewer"
            )
        key = key.replace("alt", "cmd")
        actions.key(key)


@ctx.action_class("app")
class AppActions:
    def window_close():
        actions.key("alt-f4")

    def window_next():
        actions.key("alt-tab")

    def window_previous():
        actions.key("alt-shift-tab")


@ctx.action_class("edit")
class EditActions:
    def selected_text() -> str:
        # clip.capture() always returns clip.NoChange
        clip.set_text("blah")
        actions.edit.copy()
        for i in range(20):
            text = clip.text()
            if text is not None and text != "blah":
                return text
            actions.sleep("10ms")
        else:
            return ""


@mod.action_class
class Actions:
    def window_toggle_full_screen():
        """Toggle full screen state of the frontmost window"""

    def citrix_use_all_displays_in_full_screen():
        """Toggle using all displays in full screen"""

    def windows_key(key: str):
        """Press one or more keys by name, space-separated, replacing Windows by Mac equivalents if needed"""
        if app.platform == "windows":
            actions.key(key)
            return

        raise Exception("Unexpected use of user.windows_key outside Citrix Viewer")


def on_win_focus(window):
    if window.app.bundle == "com.citrix.receiver.icaviewer.mac" and window.title == "":
        actions.user.status_add("Citrix Viewer window has no title")
    else:
        actions.user.status_remove("Citrix Viewer window has no title")


def on_ready():
    if app.platform == "mac":
        ui.register("win_focus", on_win_focus)


app.register("ready", on_ready)
