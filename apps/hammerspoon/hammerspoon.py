from talon import Context, Module, app, ui

ctx = Context()
mod = Module()

ctx.matches = r"""
os: mac
"""


def hammerspoon_app():
    return ui.apps(bundle="org.hammerspoon.Hammerspoon")[0]


@ctx.action_class("user")
class UserActions:
    def hammerspoon_menu_select(title):
        hs = hammerspoon_app().element
        if not hs.attrs:
            message = """Unable to interact with Hammerspoon. Has it hung?

            Note that you may need to restart Talon if you restart Hammerspoon."""
            app.notify(
                title="Hammerspoon",
                body=message,
            )
            raise Exception(message)
        hs_menu_extra = hs.AXExtrasMenuBar.children.find_one(
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
