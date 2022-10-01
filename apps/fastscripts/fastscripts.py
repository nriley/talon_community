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
        fastscripts.children.find_one(
            AXRole="AXMenuBarItem", AXSubrole="AXMenuExtra", max_depth=1
        ).perform("AXPress")
        actions.insert(text)


@mod.action_class
class Actions:
    def fastscripts_search(text: str):
        """Searches for a script in FastScripts"""
