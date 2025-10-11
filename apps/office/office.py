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
    def office_mail_this():
        """Attach the frontmost document to an email from an Office app"""

    def office_ribbon_select(keys: str):
        """Select from the ribbon in an Office app"""
