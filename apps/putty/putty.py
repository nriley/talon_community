from talon import Context, Module, actions, app

mod = Module()
ctx = Context()
ctx_configuration = Context()

mod.apps.putty = r"""
os: windows
and app.exe: /putty\.exe/i
"""

mod.apps.putty_configuration = """
app: putty
and win.class: PuTTYConfigBox
"""

# intentionally includes os so it's more specific than edit_win
ctx.matches = """
os: windows
app: putty
"""

ctx_configuration.matches = """
app: putty_configuration
"""

mod.list("putty_session", "PuTTY saved sessions")


@ctx.action_class("edit")
class EditActions:
    def paste():
        actions.key("shift-insert")


@mod.action_class
class Actions:
    def putty_open_menu():
        """Open the PuTTY system menu"""

    def putty_open_session(putty_session: str):
        """Open the named PuTTY session"""


@ctx.action_class("user")
class UserActions:
    def putty_open_menu():
        # When something resembling Windows accessibility is available,
        # plan to migrate to this; in the meantime, assumes that
        # Window > Behaviour > System menu appears on ALT-Space is set
        actions.key("alt-space")


@ctx_configuration.action_class("user")
class ConfigurationUserActions:
    def putty_open_session(putty_session: str):
        actions.key("alt-e")
        actions.insert(putty_session)
        actions.key("alt-l alt-o")


def ready():
    import winreg
    from urllib.parse import unquote

    hkcu = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    sessions_key = winreg.OpenKey(hkcu, r"SOFTWARE\SimonTatham\PuTTY\Sessions")
    sessions = []
    index = 0
    while True:
        try:
            sessions.append(unquote(winreg.EnumKey(sessions_key, index)))
            index += 1
        except OSError:
            break

    ctx.lists["user.putty_session"] = actions.user.create_spoken_forms_from_list(
        sessions
    )


if app.platform == "windows":
    app.register("ready", ready)
