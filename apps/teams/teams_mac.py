from talon import app, ui


def app_launched(app):
    if not app.bundle == "com.microsoft.teams":
        return

    try:
        app.element.AXManualAccessibility = True
    except ui.UIErr as e:
        pass  # expect "Error setting element attribute" even on success


if app.platform == "mac":
    ui.register("app_launch", app_launched)
