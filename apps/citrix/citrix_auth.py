from urllib.parse import urlsplit, urlunsplit

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
        auth_managers = ui.apps(bundle="com.citrix.AuthManagerMac")
        if len(auth_managers) == 1:
            auth_manager = auth_managers[0]
        elif (
            auth_manager := ui.active_app()
        ) and auth_manager.bundle == "com.citrix.AuthManagerMac":
            pass
        else:
            app.notify(
                "Unable to identify unique Citrix Workspace Authentication app; try activating it first"
            )
            return
        window = auth_manager.active_window

        # Log in with web view (makes some assumptions about form elements)
        try:
            web_area = window.children.find_one(AXRole="AXWebArea", max_depth=3)
        except ui.UIErr:
            web_area = None
        if web_area is not None:
            # Store both username and password in password field
            # as there is no way to retrieve the username with Talon's
            # keychain API <https://github.com/talonvoice/talon/issues/577>
            host_url = urlsplit(web_area.AXURL)
            host_url = urlunsplit((host_url.scheme, host_url.netloc, "/", "", ""))
            try:
                username, password = keychain.find(host_url, "").split("|", 2)
            except keychain.KeychainErr:
                app.notify(f"Failed to get keychain item for {host_url}")
                raise
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
            AXRole="AXTextField",
            AXSubrole="AXSecureTextField",
            AXRoleDescription="passwd",
        )
        passwd.AXValue = keychain.find("Citrix Workspace", username)
        submit = window.children.find_one(AXRole="AXButton", AXRoleDescription="submit")
        submit.perform("AXPress")


@mod.action_class
class Actions:
    def citrix_sign_in():
        """Sign into Citrix Workspace."""
