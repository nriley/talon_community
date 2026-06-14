from talon import Context, Module, actions

mod = Module()
ctx_mac = Context()

ctx_mac.matches = r"""
os: mac
"""


@mod.action_class
class Actions:
    def copy_style():
        """Copies the style of the selection to the clipboard"""

    def paste_style():
        """Applies the copied style to the selection"""

    def clear_style():
        """Clears style information from the selection"""

    def normal_style():
        """Applies the “Normal” style to the selection"""
        actions.user.clear_style()


@ctx_mac.action_class("user")
class MacUserActions:
    def copy_style():
        actions.key("cmd-alt-c")

    def paste_style():
        actions.key("cmd-alt-v")

    def clear_style():
        actions.key("cmd-ctrl-backspace")
