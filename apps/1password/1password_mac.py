from talon import Context, actions, ui

ctx = Context()

# i don't see a need to restrict the app here, this just defines the actions
# each app can support appropriate voice commands as needed
# the below are for 1password, redefine as needed
ctx.matches = r"""
os: mac
"""


@ctx.action_class("user")
class UserActions:
    def password_fill():
        # Autofill keyboard shortcut in General Settings
        actions.key("cmd-alt-shift-\\")

    def password_show():
        # Show Quick Access keyboard shortcut in General Settings
        actions.key("cmd-alt-\\")

    def password_new():
        actions.key("cmd-i")

    def password_duplicate():
        actions.key("cmd-d")

    def password_edit():
        actions.key("cmd-e")

    def password_delete():
        actions.key("cmd-backspace")

    def password_search(text: str):
        actions.user.password_show()
        focused_element = None
        search_field = None
        for attempt in range(200):
            actions.sleep("50ms")
            try:
                focused_element = ui.focused_element()
            except RuntimeError:
                continue
            if focused_element is None:
                continue
            try:
                window = focused_element.window
            except ui.UIErr:
                print(f"Unable to find window for focused element: {focused_element}")
                continue
            if window.app.bundle != "com.1password.1password":
                continue
            if not (window_element := focused_element.get("AXWindow")):
                continue
            if window_element.get("AXModal") or window_element.get("AXCloseButton"):
                continue  # not the Quick Access window
            if (  # empty search field focused
                focused_element.get("AXRole") == "AXTextField"
                and focused_element.get("AXSubrole") == "AXSearchField"
            ):
                search_field = focused_element
                break
            # something else focused; find the search field
            try:
                search_field = window_element.children.find_one(
                    AXRole="AXTextField", AXSubrole="AXSearchField"
                )
            except ui.UIErr:
                print(f"Unable to find search field in {window_element}")
                continue
            break
        else:
            if focused_element is None:
                print(
                    f"Did not find any focused element, but frontmost window is {ui.active_window()}"
                )
            else:
                print(f"Found focused element: {focused_element.dump()}")
            raise Exception("Gave up waiting for 1Password Quick Access")
        for attempt in range(10):
            search_field.AXValue = text
            actions.sleep("50ms")
            if search_field.AXValue == text:
                return
        raise Exception("Gave up waiting to set 1Password Quick Access search string")
