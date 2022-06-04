from talon import Module, app, ui

mod = Module()


def unc_app():
    apps = ui.apps(bundle="com.apple.UserNotificationCenter")
    if not apps:
        app.notify("UserNotificationCenter is not running")
        return None
    return apps[0]


def unc_alert():
    unc = unc_app()
    if not unc:
        return

    window = unc.active_window.element
    if not window.get("AXSubrole") == "AXSystemDialog":
        return None
    return window


@mod.action_class
class Actions:
    def unc_alert_dismiss():
        """Dismiss the frontmost UserNotificationCenter alert"""
        alert = unc_alert()
        if not alert:
            app.notify("No active UserNotificationCenter alert to dismiss")
            return
        alert.AXDefaultButton.perform("AXPress")
