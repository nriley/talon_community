from talon import Context, Module, actions, app, keychain, registry, ui

mod = Module()
ctx = Context()

mod.apps.putty = """
os: windows
and app.exe: putty.exe
"""

ctx.matches = """
app: putty
"""

mod.list("putty_session", "PuTTY saved sessions")


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


from talon import app

if app.platform == "windows":
    app.register("ready", ready)
