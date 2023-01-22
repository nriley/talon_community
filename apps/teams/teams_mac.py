from talon import app, ui


def app_launched(app):
    if not app.bundle == "com.microsoft.teams":
        return

    app.element.AXEnhancedUserInterface = True


if app.platform == "mac":
    ui.register("app_launch", app_launched)
