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
        actions.key("cmd-shift-x")

    def password_show():
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
        for attempt in range(10):
            actions.sleep("50ms")
            try:
                focused_element = ui.focused_element()
                if (
                    focused_element.AXRole == "AXTextField"
                    and focused_element.AXDOMIdentifier == "quick-access-search"
                ):
                    break
            except:
                pass
        else:
            print("Gave up waiting for quick access search")
            return
        for attempt in range(10):
            focused_element.AXValue = text
            actions.sleep("50ms")
            if focused_element.AXValue == text:
                return
        print("Gave up waiting to set search string")
