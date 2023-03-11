from talon import Context, Module, actions, ui

ctx = Context()
mod = Module()

ctx.matches = r"""
os: mac
"""


@ctx.action_class("user")
class UserActions:
    def fastscripts_search(text: str):
        fastscripts = ui.apps(bundle="com.red-sweater.fastscripts3")[0]
        menu_extra = fastscripts.children.find_one(
            AXRole="AXMenuBarItem", AXSubrole="AXMenuExtra", max_depth=1
        )
        menu_extra.perform("AXPress")
        for attempt in range(10):
            actions.sleep("50ms")
            try:
                search_field = menu_extra.children.find_one(
                    AXRole="AXTextField", AXSubrole="AXSearchField"
                )
                break
            except:
                pass
        else:
            print("Unable to find FastScripts search field")
            return
        search_field.AXValue = text


@mod.action_class
class Actions:
    def fastscripts_search(text: str):
        """Searches for a script in FastScripts"""
