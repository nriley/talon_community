from talon import Context, Module, app, ctrl, ui


def hidden_bar():
    return ui.apps(bundle="com.dwarvesv.minimalbar")[0]


mod = Module()
ctx = Context()

ctx.matches = r"""
os: mac
"""


@mod.action_class
class Actions:
    def status_area_toggle_expansion():
        """Toggle display of additional items in the OS status area"""


@ctx.action_class("user")
class UserActions:
    def status_area_toggle_expansion():
        hb = hidden_bar()
        for menu_extra in hb.children.find(
            AXRole="AXMenuBarItem", AXSubrole="AXMenuExtra"
        ):
            if menu_extra.AXFrame.width < 5000:
                break
        else:
            raise RuntimeError("Unable to find Hidden Bar menu extra")

        mouse_pos = ctrl.mouse_pos()
        ctrl.mouse_move(*menu_extra.AXFrame.center)
        ctrl.mouse_click()
        ctrl.mouse_move(*mouse_pos)
