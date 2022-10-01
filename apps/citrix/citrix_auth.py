from talon import Context, Module, actions, app, keychain, ui

mod = Module()
ctx = Context()

ctx.matches = """
os: mac
and app.bundle: com.citrix.AuthManagerMac
"""


@ctx.action_class("user")
class UserActions:
    def citrix_sign_in():
        citrix_auth = ui.apps(bundle="com.citrix.AuthManagerMac")[0]
        # XXX have to focus another app then back to the app or the window will not show up
        ui.apps(bundle="com.apple.finder")[0].focus()
        actions.sleep("100ms")
        citrix_auth.focus()
        for attempt in range(10):
            windows = citrix_auth.windows()
            if len(windows) == 0:
                actions.sleep("100ms")
                continue
            window = citrix_auth.windows()[0]
            break
        else:
            app.notify("Gave up while waiting for window")
            return
        login = window.children.find_one(
            AXRole="AXTextField", AXRoleDescription="login"
        )
        username = login["AXValue"]
        passwd = window.children.find_one(
            AXRole="AXTextField", AXRoleDescription="passwd"
        )
        passwd["AXValue"] = keychain.find("Citrix Workspace", username)
        submit = window.children.find_one(AXRole="AXButton", AXRoleDescription="submit")
        submit.perform("AXPress")


@mod.action_class
class Actions:
    def citrix_sign_in():
        """Sign into Citrix Workspace."""
