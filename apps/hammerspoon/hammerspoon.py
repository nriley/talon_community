from talon import Context, Module, ui

ctx = Context()
mod = Module()

ctx.matches = r"""
os: mac
"""


@ctx.action_class("user")
class UserActions:
    def hammerspoon_menu_select(title):
        hs = ui.apps(bundle="org.hammerspoon.Hammerspoon")[0]
        hs_menu_extra = hs.element.AXExtrasMenuBar.children.find_one(
            AXRole="AXMenuBarItem", AXSubrole="AXMenuExtra", max_depth=0
        )
        try:
            hs_menu_extra.perform("AXPress")
        except:
            pass  # This appears to fail but doesn't
        hs_menu_extra.children.find_one(AXRole="AXMenuItem", AXTitle=title).perform(
            "AXPress"
        )


@mod.action_class
class Actions:
    def hammerspoon_menu_select(title: str):
        """Select the specified item from the Hammerspoon menu"""
