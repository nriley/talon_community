from talon import Context, Module, actions

mod = Module()

mod.apps.office = r"""
app: office_mac
app: office_win
"""

ctx = Context()
ctx.matches = r"""
app: office
"""


@mod.action_class
class Actions:
    def office_tell_me():
        """Focus 'Tell me' in Microsoft Office apps"""


@ctx.action_class("user")
class UserActions:
    # user.command_search
    def command_search(command=""):
        actions.user.office_tell_me()
        if command != "":
            actions.insert(command)
