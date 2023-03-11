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

        # Log in with web view (makes some assumptions about form elements)
        if web_area := window.children.find_one(AXRole="AXWebArea", max_depth=3):
            # Store both username and password in password field
            # as there is no way to retrieve the username with Talon's
            # keyboard API <https://github.com/talonvoice/talon/issues/577>
            username, password = keychain.find(web_area.AXURL, "").split("|", 2)
            login = web_area.children.find_one(AXRole="AXTextField", AXSubrole=None)
            login.AXValue = username
            passwd = web_area.children.find_one(
                AXRole="AXTextField", AXSubrole="AXSecureTextField"
            )
            passwd.AXFocused = True
            actions.paste(password)
            submit = web_area.children.find_one(AXRole="AXButton")
            submit.perform("AXPress")
            return

        # Log in with native UI
        login = window.children.find_one(
            AXRole="AXTextField", AXRoleDescription="login"
        )
        username = login.AXValue
        passwd = window.children.find_one(
            AXRole="AXTextField", AXRoleDescription="passwd"
        )
        passwd.AXValue = keychain.find("Citrix Workspace", username)
        submit = window.children.find_one(AXRole="AXButton", AXRoleDescription="submit")
        submit.perform("AXPress")


@mod.action_class
class Actions:
    def citrix_sign_in():
        """Sign into Citrix Workspace."""
