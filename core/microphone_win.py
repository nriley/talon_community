from talon import Context, Module, actions, app, scope, ui

mod = Module()
ctx = Context()
ctx.matches = """
os: windows
"""


def ui_callback(event, app):
    if event not in ("app_launch", "app_close"):
        return
    if app.exe or app.name != "LogonUI.exe":
        return
    if event == "app_launch":
        actions.speech.disable()
        return

    print(event, app)


if app.platform == "windows":
    ui.register("", ui_callback)
