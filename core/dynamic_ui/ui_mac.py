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
        element.perform("AXPress")

    def ui_element_focus(element):
        element.AXFocused = True

    def ui_element_hover(element):
        ctrl.mouse_move(*element.AXFrame.center)

    def ui_element_menu(element):
        element.AXFocused = True
        element.perform("AXShowMenu")


def active_window_elements(*roles):
    parent = ui.active_window().element
    # don't expose the contents of the window to which a sheet is attached
    with suppress(ui.UIErr):
        parent = parent.children.find_one(AXRole="AXSheet", max_depth=0)

    element_dict = {}
    for role in roles:
        for element in parent.children.find(AXRole=role):
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
                        titles.append(str(value))
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
            "AXRadioButton",
            "AXPopUpButton",
            "AXDisclosureTriangle",
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
