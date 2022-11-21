from talon import Context, Module, actions, ui

mod = Module()
ctx = Context()
ctx.matches = """
os: mac
"""


@mod.action_class
class Action:
    def citrix_focus_desktop() -> bool:
        """Focus the Citrix desktop, returning whether successful"""

    def citrix_focus_workspace():
        """Focus Citrix Workspace"""


@ctx.action_class("user")
class UserActions:
    def citrix_focus_desktop():
        for viewer in ui.apps(bundle="com.citrix.receiver.icaviewer.mac"):
            # XXX work around the subrole being AXDialog when the app is hidden
            was_hidden = viewer.element.AXHidden
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
