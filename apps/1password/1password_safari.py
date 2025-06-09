from talon import Context, Module, actions, ui

ctx = Context()
mod = Module()

ctx.matches = r"""
app: safari
"""


@mod.action_class
class Actions:
    def browser_focus_password_autofill():
        """Focus the password autofill area"""


@ctx.action_class("user")
class UserActions:
    def browser_focus_password_autofill():
        window = ui.active_window()
        if not window:
            return
        if not (sections := getattr(window.element, "AXSections")):
            return
        content = next(
            o["SectionObject"] for o in sections if o["SectionUniqueID"] == "AXContent"
        )
        autofill = next(
            o
            for o in content.children.find(AXRole="AXWebArea")
            if o.AXURL.startswith(
                "safari-web-extension://506D2125-AA38-4102-9097-3F6F2FDDC127"
            )
        )
        autofill.AXFocused = True
