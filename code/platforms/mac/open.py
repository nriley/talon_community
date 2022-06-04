from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
"""


@ctx.action_class("user")
class UserActions:
    def file_open():
        actions.key("cmd-o")
