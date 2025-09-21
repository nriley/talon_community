from contextlib import suppress

from talon import Context, Module, actions, app, ctrl, ui

mod = Module()
ctx = Context()

ctx.matches = r"""
os: mac
"""


@mod.action_class
class Actions:
    def ui_element_click(element: ui.Element):
        """Click on a UI element"""

    def ui_element_focus(element: ui.Element):
        """Move keyboard focus to a UI element"""

    def ui_element_hover(element: ui.Element):
        """Move the mouse pointer to a UI element"""

    def ui_element_menu(element: ui.Element):
        """Show a menu on a UI element"""


@ctx.action_class("user")
class UserActions:
    def ui_element_click(element):
        with suppress(ui.ActionFailed):
            element.perform("AXPress")

    def ui_element_focus(element):
        element.AXFocused = True
        if not element.AXFocused:
            previous_position = ctrl.mouse_pos()
            actions.user.ui_element_hover(element)
            ctrl.mouse_click()
            ctrl.mouse_move(*previous_position)

    def ui_element_hover(element):
        ctrl.mouse_move(*element.AXFrame.center)

    def ui_element_menu(element):
        if element.AXRole == "AXComboBox":
            element.children.find_one(AXRole="AXButton", max_depth=0).perform("AXPress")
            return
        element.AXFocused = True
        element.perform("AXShowMenu")


def active_window_elements(*roles):
    window = ui.active_window()
    if window.id == -1:
        # XXX core Talon bug? You get Window(None) instead of None
        # even though there is a focused window (e.g. sheet in Installer)
        parent = ui.active_app().element.AXFocusedWindow
    else:
        parent = ui.active_window().element
    if parent.AXRole != "AXSheet":
        # don't expose the contents of the window to which a sheet is attached
        with suppress(ui.UIErr):
            parent = parent.children.find_one(AXRole="AXSheet", max_depth=0)

    element_dict = {}
    for role in roles:
        # Some apps (e.g., Excel's Create Table dialog) have loops in their
        # accessibility hierarchy; pick a large maximum depth to avoid
        # searching forever and hopefully not miss anything important
        for element in parent.children.find(AXRole=role, max_depth=50):
            titles = []
            if (
                role != "AXRadioButton"
                and (title_element := getattr(element, "AXTitleUIElement", None))
                and (title := getattr(title_element, "AXValue", None))
            ):
                titles.append(title)
            else:
                for attr in (
                    "AXTitle",
                    "AXDescription",
                    "AXAttributedDescription",
                    "AXHelp",
                ):
                    if title := getattr(element, attr, None):
                        titles.append(title)
                        break
                else:
                    if identifier := getattr(element, "AXIdentifier", None):
                        if not identifier.startswith("_") and not identifier.endswith(
                            ":"
                        ):
                            titles.append(identifier)

            if role in ("AXPopUpButton", "AXTextField", "AXComboBox"):
                for attr in (
                    "AXValue",
                    "AXPlaceholderValue",
                ):
                    if value := getattr(element, attr, None):
                        titles.append(str(value) + "\n")
                        break

            for title in titles:
                element_dict[title] = element

    return element_dict


def on_ready():
    actions.user.ui_dynamic_list_and_capture(
        "button in active window",
        ctx,
        mod.list("ui_active_window_button", desc="Buttons in active window"),
        lambda: active_window_elements(
            "AXButton",
            "AXCheckBox",
            "AXColorWell",
            "AXDisclosureTriangle",
            "AXMenuButton",
            "AXPopUpButton",
            "AXRadioButton",
        ),
        lambda e: e,
    )
    actions.user.ui_dynamic_list_and_capture(
        "text field in active window",
        ctx,
        mod.list("ui_active_window_field", desc="Text fields in active window"),
        lambda: active_window_elements("AXTextArea", "AXTextField", "AXComboBox"),
        lambda e: e,
    )


app.register("ready", on_ready)
