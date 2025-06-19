from pathlib import Path

from talon import Context, Module, actions, ui

mod = Module()
ctx = Context()
ctx.matches = """
os: mac
"""


@mod.action_class
class Actions:
    def citrix_focus_desktop() -> bool:
        """Focus the Citrix desktop, returning whether successful"""

    def citrix_focus_workspace():
        """Focus Citrix Workspace"""

    def citrix_launch_favorite(favorite: str):
        """Launch the specified Citrix app or desktop"""

    def citrix_focus_app(app_name: str) -> bool:
        """Focus a Citrix app, returning whether successful"""

    def citrix_launch_or_focus(favorite: str):
        """Focus a Citrix app if running, otherwise launch it"""


@ctx.action_class("user")
class UserActions:
    def citrix_focus_desktop():
        for viewer in ui.apps(bundle="com.citrix.receiver.icaviewer.mac"):
            # XXX work around the subrole being AXDialog when the app is hidden
            was_hidden = getattr(viewer.element, "AXHidden", False)
            if was_hidden is True:
                viewer.element.AXHidden = False
            for window in viewer.windows():
                if window.element.get("AXSubrole") == "AXStandardWindow":
                    actions.user.switcher_save_mouse_pos()
                    viewer.focus()
                    window.focus()
                    actions.user.switcher_restore_mouse_pos(window.app)
                    return True
            if was_hidden:
                viewer.element.AXHidden = True
        else:
            return False

    def citrix_focus_workspace():
        actions.user.launch_or_focus_bundle("com.citrix.receiver.nomas")

    def citrix_focus_app(app_name):
        for husk in ui.apps(bundle="com.citrix.ctxapphusk"):
            husk_name = Path(husk.exe).parents[2].stem
            if app_name.startswith(husk_name):
                actions.user.switcher_save_mouse_pos()
                husk.focus()
                for attempt in range(10):
                    actions.sleep("10ms")
                    active_app = ui.active_app()
                    if active_app.bundle == "com.citrix.receiver.icaviewer.mac":
                        break
                else:
                    raise ("Timed out waiting to focus Citrix Viewer")
                    return False
                actions.user.switcher_restore_mouse_pos(ui.active_app())
        else:
            return False

        return True

    def citrix_launch_or_focus(favorite):
        if actions.user.citrix_focus_app(favorite):
            return

        actions.user.citrix_launch_favorite(favorite)
