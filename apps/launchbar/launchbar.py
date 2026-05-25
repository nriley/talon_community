from talon import Context, Module, actions

ctx = Context()
mod = Module()

ctx.matches = r"""
os: mac
"""


def launchbar_app():
    import appscript

    return appscript.app(id="at.obdev.LaunchBar")


@ctx.action_class("user")
class UserActions:
    def launchbar_action(action: str, argument: str):
        launchbar = launchbar_app()
        if argument:
            launchbar.perform_action(action, with_string=argument)
        else:
            launchbar.perform_action(action)

    def launchbar_select(text: str):
        launchbar = launchbar_app()
        from urllib.parse import quote

        abbreviation = actions.user.formatted_text(text, "ALL_LOWERCASE,NO_SPACES")
        launchbar.open_location(
            "x-launchbar:select?abbreviation=" + quote(abbreviation)
        )


@mod.action_class
class Actions:
    def launchbar_action(action: str, argument: str):
        """Performs the LaunchBar action with an (optional) specified argument"""

    def launchbar_select(text: str):
        """Selects an abbreviation in LaunchBar"""
