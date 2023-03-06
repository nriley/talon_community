from typing import Optional

from appscript import k
from talon import Context, Module, actions, cron, ui

mod = Module()
ctx = Context()

ctx.matches = """
os: mac
and app.bundle: com.omnigroup.OmniFocus3.MacAppStore
"""


def omnifocus_app():
    return ui.apps(bundle="com.omnigroup.OmniFocus3.MacAppStore")[0]


@ctx.action_class("user")
class UserActions:
    def omnifocus_complete():
        content = omnifocus_app().appscript().windows[1].content
        # get the selected trees (by index)
        selected_trees = content.selected_trees()
        # mark each tree (by ID) as complete
        content.selected_trees.value.mark_complete()
        # restore the selected trees
        # (which may be different now if cleanup happens immediately)
        cron.after(
            "300ms",
            lambda: content.selected_trees.set(
                [tree for tree in selected_trees if tree.exists()]
            ),
        )

    def omnifocus_postpone(days: Optional[int]):
        actions.key("ctrl-cmd-l")
        if days:
            actions.insert(str(days))

    def omnifocus_select_tree(tree: str):
        from talon.mac import applescript

        applescript.run(
            f'tell application id "com.omnigroup.OmniFocus3.MacAppStore" to tell window 1\'s content to set selected trees to {{{tree}}}'
        )
        actions.key("alt-cmd-2")

    def find_everywhere(text: str):
        actions.key("alt-cmd-f")
        actions.insert(text)


@mod.action_class
class Actions:
    def omnifocus_complete():
        """Mark the selection as completed while preserving the selection"""

    def omnifocus_postpone(days: Optional[int]):
        """Postpone by a number of days"""

    def omnifocus_select_tree(tree: str):
        """Select a tree in the outline (specified as AppleScript scoped to window content)"""
