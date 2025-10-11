from contextlib import suppress
from enum import StrEnum
from operator import itemgetter
from typing import Optional, Union

from talon import Context, Module, actions, app, ctrl, ui
from talon.types import Span

mod = Module()
ctx = Context()

ctx.matches = r"""
os: mac
"""

mod.list("scroll_direction", "Scroll direction")


class AXScrollByPageAction(StrEnum):
    # most (but not all) apps reverse this
    AXScrollDownByPage = "UP"
    AXScrollUpByPage = "DOWN"
    AXScrollRightByPage = "LEFT"
    AXScrollLeftByPage = "RIGHT"


@mod.action_class
class Actions:
    def ui_element_active_window_or_sheet() -> ui.Element:
        """Return a UI element for the active window or sheet"""

    def ui_element_click(element: ui.Element):
        """Click on a UI element"""

    def ui_element_focus(element: ui.Element):
        """Move keyboard focus to a UI element"""

    def ui_element_hover(element: ui.Element):
        """Move the mouse pointer to a UI element"""

    def ui_element_menu(element: ui.Element):
        """Show a menu on a UI element"""

    def ui_element_select(element: ui.Element):
        """Select a UI element"""

    def ui_element_end(tail: Optional[bool] = False, select: Optional[bool] = False):
        """Go to one end of the focused UI element (head, beginning or first item)"""

    def ui_element_scroll(direction: Union[str, AXScrollByPageAction]):
        """Scroll the focused UI element"""


@ctx.action_class("user")
class UserActions:
    def ui_element_active_window_or_sheet():
        window = ui.active_window()
        if window.id == -1:
            # XXX core Talon bug? You get Window(None) instead of None
            # even though there is a focused window (e.g. sheet in Installer)
            parent = ui.active_app().element.AXFocusedWindow
        else:
            parent = window.element
        if getattr(parent, "AXRole", None) != "AXSheet":
            # don't expose the contents of the window to which a sheet is attached
            with suppress(ui.UIErr):
                parent = parent.children.find_one(AXRole="AXSheet", max_depth=0)

        return parent

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
        match element.AXRole:
            case "AXComboBox":
                # focusing is not necessary to pop up the menu,
                # but lets you use "row" commands
                actions.user.ui_element_focus(element)
                # selecting is not necessary to pop up the menu,
                # but helps if you insert a replacement
                selected_range = Span(0, element.AXNumberOfCharacters)
                for attempt in range(10):
                    element.AXSelectedTextRange = selected_range
                    if element.AXSelectedTextRange == selected_range:
                        break
                    actions.sleep("10ms")
                with suppress(ui.ActionFailed):
                    element.children.find_one(AXRole="AXButton", max_depth=0).perform(
                        "AXPress"
                    )
                return
            case "AXRow":
                for child in element.children.find(max_depth=1):
                    if "AXShowMenu" in child.actions:
                        with suppress(ui.ActionFailed):
                            child.perform("AXShowMenu")
                        return
                previous_position = ctrl.mouse_pos()
                actions.user.ui_element_hover(element)
                ctrl.mouse_click(1)
                ctrl.mouse_move(*previous_position)
                return

        with suppress(ui.UIErr):
            element.AXFocused = True
        with suppress(ui.ActionFailed):
            element.perform("AXShowMenu")

    def ui_element_select(element):
        parent = element.parent
        for attr in ("AXSelectedRows", "AXSelectedChildren"):
            if selected := getattr(parent, attr, None):
                if vs := getattr(parent.parent, "AXVerticalScrollBar", None):
                    children = list(parent.children)
                    index = children.index(element)
                    # Assumes equal row height
                    vs.AXValue = index / len(children)
                with suppress(ui.UIErr):
                    setattr(parent, attr, [element])
                break
        with suppress(ui.UIErr):
            element.AXSelected = True

    def ui_element_end(tail=False, select=False):
        element = actions.user.focused_element_safe()
        if element is None:
            return
        if (range := getattr(element, "AXSelectedTextRange", None)) is not None:
            # For text, move the insertion point by default
            if tail:
                if length := getattr(element, "AXNumberOfCharacters", None):
                    element.AXSelectedTextRange = Span(
                        range.left if select else length, length
                    )
                else:
                    raise RuntimeError("Unable to get character count")
            else:
                element.AXSelectedTextRange = Span(0, range.right if select else 0)
            return
        if vs := getattr(element.parent, "AXVerticalScrollBar", None):
            # For a list/table/outline or anything else scrollable, scroll by default
            vs.AXValue = 1 if tail else 0
            if select:
                if hasattr(element, "AXSelectedRows") and (
                    rows := getattr(element, "AXVisibleRows")
                ):
                    with suppress(ui.UIErr):
                        rows[-1 if tail else 0].AXSelected = True
                elif hasattr(element, "AXSelectedChildren"):
                    if tail:
                        child = element.children.find(max_depth=0)[-1]
                    else:
                        child = element.children.find_one()
                    element.AXSelectedChildren = [child]
            return

    def ui_element_scroll(direction):
        element = ui.focused_element()

        action = AXScrollByPageAction(direction).name
        while True:
            element = element.parent
            match element.AXRole:
                case "AXScrollArea":
                    break
                case ("AXWindow", "AXApplication"):
                    raise Exception("Unable to find a scroll area")

        if action not in element.actions:
            raise Exception(f"Scroll area does not implement {action}")

        with suppress(ui.ActionFailed):
            element.perform(action)


def active_window_elements(*roles):
    parent = actions.user.ui_element_active_window_or_sheet()

    element_dict = {}
    for role in roles:
        for element in parent.children.find(AXRole=role, visible_only=True):
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
                    "AXRoleDescription",
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


def list_rows(element, all=False):
    element_dict = {}
    rows = getattr(element, "AXRows" if all else "AXVisibleRows", [])
    i = 1
    for row in rows:
        titles = []
        for role in ("AXStaticText", "AXTextField"):
            for text in row.children.find(AXRole=role):
                if title := getattr(text, "AXValue", None):
                    titles.append([text.AXPosition.y, text.AXPosition.x, title])
        if not titles:
            continue

        titles.sort()
        element_dict[f"{i}. " + " - ".join(title for top, left, title in titles)] = row
        i += 1

    return element_dict


def combo_box_rows(element):
    element_dict = {}
    list = element.children.find_one(AXRole="AXList", max_depth=1)
    i = 1
    for text in list.children:
        if title := getattr(text, "AXValue", None):
            if str.isnumeric(title):
                element_dict[title] = text
            else:
                element_dict[f"{i}. {title}"] = text
                i += 1

    return element_dict


def focused_list_rows(all=False):
    element = actions.user.focused_element_safe()
    if not element:
        return {}

    if element.AXRole == "AXComboBox":
        return combo_box_rows(element)

    return list_rows(element, all)


def sidebar_rows():
    # Doesn't identify sidebars in Catalyst apps
    parent = actions.user.ui_element_active_window_or_sheet()
    for depth in range(3):
        for split in parent.children.find(AXRole="AXSplitGroup", max_depth=depth):
            if scroll_areas := split.children.find(AXRole="AXScrollArea", max_depth=2):
                frame_scroll = [(sa.AXFrame.left, sa) for sa in scroll_areas]
                frame_scroll.sort(key=itemgetter(0))
                for _, sa in frame_scroll:
                    scroll_child = sa.children[0]
                    if scroll_child.AXRole in ("AXOutline", "AXTable"):
                        if rows := list_rows(scroll_child, True):
                            return rows
    else:
        return {}


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
    actions.user.ui_dynamic_list_and_capture(
        "list, table or outline in active window",
        ctx,
        mod.list(
            "ui_active_window_list", desc="Lists, tables and outlines in active window"
        ),
        lambda: active_window_elements("AXTable", "AXOutline"),
        lambda e: e,
    )
    actions.user.ui_dynamic_list_and_capture(
        "visible rows of focused list, table or outline",
        ctx,
        mod.list(
            "ui_focused_list_visible_row",
            desc="Visible rows of focused list, table or outline",
        ),
        focused_list_rows,
        lambda e: e,
    )
    actions.user.ui_dynamic_list_and_capture(
        "rows of focused list, table or outline",
        ctx,
        mod.list("ui_focused_list_row", desc="Rows of focused list, table or outline"),
        lambda: focused_list_rows(True),
        lambda e: e,
    )
    actions.user.ui_dynamic_list_and_capture(
        "rows of sidebar",
        ctx,
        mod.list("ui_sidebar_row", desc="Rows of sidebar"),
        sidebar_rows,
        lambda e: e,
    )


app.register("ready", on_ready)
