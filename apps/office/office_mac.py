import re
from collections.abc import Callable
from contextlib import suppress
from typing import Optional

from talon import Context, Module, actions, app, ctrl, ui

mod = Module()
ctx = Context()

mod.apps.excel_mac = """
os: mac
and app.bundle: com.microsoft.Excel
"""
mod.apps.onenote_mac = r"""
os: mac
and app.bundle: com.microsoft.onenote.mac
"""
mod.apps.powerpoint_mac = r"""
os: mac
and app.bundle: com.microsoft.Powerpoint
"""
mod.apps.word_mac = r"""
os: mac
and app.bundle: com.microsoft.Word
"""
mod.apps.office_mac = r"""
app: excel_mac
app: onenote_mac
app: powerpoint_mac
app: word_mac
"""

ctx.matches = """
app: office_mac
"""


def document_window_toolbar_group():
    window = actions.user.office_mac_document_window()
    try:
        toolbar = window.children.find_one(AXRole="AXToolbar", max_depth=0)
    except ui.UIErr:
        # full screen includes an additional layer
        group = next(
            e
            for e in window.children.find(AXRole="AXGroup", max_depth=0)
            if not hasattr(e, "AXDescription")
        )
        toolbar = group.children.find_one(AXRole="AXToolbar", max_depth=0)
    return toolbar.children.find_one(AXRole="AXGroup", max_depth=0)


def document_window_tab_group():
    return actions.user.office_mac_document_window().children.find_one(
        AXRole="AXTabGroup", max_depth=0
    )


@mod.action_class
class Actions:
    def office_document_actions():
        """Opens the document actions popover"""

    def office_mac_document_window():
        """Returns the current document window"""

    def office_mac_ribbon_activate_tab(
        tab_index: int, tab_name: str
    ) -> Optional[ui.Element]:
        """Activates a ribbon tab by index, returning ribbon or None on failure"""

    def office_mac_ribbon_combo_box(
        tab_index: int,
        tab_name: str,
        box_name: str,
        box_filter: Optional[Callable[[ui.Element], bool]] = None,
    ) -> Optional[ui.Element]:
        """Returns a ribbon combo box by tab index and name or filter"""

    def office_mac_ribbon_control(
        tab_index: int,
        tab_name: str,
        role: str,
        name: str,
        filter: Optional[Callable[[ui.Element], bool]] = None,
    ) -> Optional[ui.Element]:
        """Returns a ribbon control by tab index and name or filter"""

    def office_mac_ribbon_control_press(
        tab_index: int,
        tab_name: str,
        role: str,
        name: str,
        filter: Optional[Callable[[ui.Element], bool]] = None,
    ) -> Optional[ui.Element]:
        """Presses a ribbon control by tab index and name or filter"""

    def office_mac_ribbon_item_select(ribbon_item: ui.Element):
        """Select the specified ribbon control"""

    def office_mac_ribbon_item_hover(ribbon_item: ui.Element):
        """Move the mouse pointer to the specified ribbon control"""

    def office_mac_ribbon_menu_select(ribbon_menu: ui.Element):
        """Open the specified ribbon menu or select a ribbon menu item"""


@ctx.action_class("user")
class UserActions:
    def office_mac_document_window():
        active_app = ui.active_app()
        try:
            for attempt in range(10):
                try:
                    window = active_app.children.find_one(
                        AXRole="AXWindow", AXSubrole="AXStandardWindow", max_depth=0
                    )
                except (AttributeError, ui.UIErr):
                    # XXX Microsoft Word sometimes returns an invalid/empty element
                    actions.sleep("10ms")
                else:
                    return window
            else:
                raise Exception(
                    f"Can't get children of {active_app.name} after {attempt} tries"
                )
        except Exception as e:
            app.notify(body="Can't find document window", title=ui.active_app().name)
            e.add_note("Unable to find a document window")
            raise

    def office_mac_ribbon_activate_tab(tab_index, tab_name):
        ribbon = document_window_tab_group()
        tab = ribbon.AXTabs[tab_index]
        if tab.get("AXValue") != 1:
            tab.perform("AXPress")

        for attempt in range(10):
            actions.sleep("50ms")
            if tab.get("AXValue") == 1:
                break
        else:
            app.notify(
                body=f"Could not activate {tab_name} tab", title=ui.active_app().name
            )
            return None

        return ribbon

    def office_mac_ribbon_control(tab_index, tab_name, role, name, filter=None):
        if (
            ribbon := actions.user.office_mac_ribbon_activate_tab(tab_index, tab_name)
        ) is None:
            return None

        controls = []
        for attempt in range(10):
            actions.sleep("50ms")
            if controls := ribbon.children.find(AXRole=role):
                break
        else:
            app.notify(
                body="Could not find ribbon controls", title=ui.active_app().name
            )
            return None

        for control in controls:
            if (
                getattr(control, "AXTitle", None) == name
                or getattr(control, "AXDescription", None) == f"{name}:"
                or (filter and filter(control))
            ):
                return control
        else:
            app.notify(
                body=f"Could not find {name} in ribbon", title=ui.active_app().name
            )
            return None

    def office_mac_ribbon_control_press(tab_index, tab_name, role, name, filter=None):
        if (
            control := actions.user.office_mac_ribbon_control(
                tab_index, tab_name, role, name, filter
            )
        ) is None:
            return None

        control.perform("AXPress")

    def office_mac_ribbon_combo_box(tab_index, tab_name, box_name, box_filter=None):
        return actions.user.office_mac_ribbon_control(
            tab_index, tab_name, "AXComboBox", box_name, box_filter
        )

    def office_ribbon_select(keys):
        # assumes KeyTips activation keystroke is set to Option-Shift
        # in Settings > Accessibility
        active_app = ui.active_app()

        def keytips_active():
            return (
                len(
                    active_app.element.children.find(AXRole="AXStaticText", max_depth=0)
                )
                > 0
            )

        if keytips_active():
            ctrl.key_press("shift", alt=True, app=active_app)
            for attempt in range(10):
                if not keytips_active():
                    break
                actions.sleep("10ms")
            else:
                error = "Unable to deactivate KeyTips. Is the activation keystroke set to something other than ⇧⌥?"
                actions.app.notify(error, active_app.AXTitle)
                raise RuntimeError(error)

        ctrl.key_press("shift", alt=True, app=active_app)
        for attempt in range(10):
            if keytips_active():
                break
            actions.sleep("10ms")
        else:
            error = "Unable to activate KeyTips. Is the activation keystroke set to something other than ⇧⌥?"
            actions.app.notify(error, active_app.AXTitle)
            raise RuntimeError(error)

        actions.key(" ".join(keys))

    def command_search(command=""):
        with suppress(ui.UIErr):
            # OneNote only as of 6/9/2025
            document_window_tab_group().children.find_one(
                AXRole="AXButton", AXTitle="Tell me", max_depth=0
            ).perform("AXPress")

            actions.key("cmd-a")
            if command != "":
                actions.insert(command)
                actions.key("down")
            else:
                actions.key("delete")
            return

        try:
            toolbar_group = document_window_toolbar_group()
        except ui.UIErr:
            raise Exception(f"Unable to locate window toolbar")
        try:
            search_field = toolbar_group.children.find_one(
                AXRole="AXTextField", AXSubrole="AXSearchField", max_depth=0
            )
            search_field.AXFocused = True
        except ui.UIErr:
            raise Exception("Unable to locate Search button")

        search_field.AXValue = command
        if command == "":
            # focusing doesn't move keyboard focus if the menu is shown
            ctrl.mouse_move(*search_field.AXFrame.center)
            ctrl.mouse_click()
            return

        active_app = ui.active_app()
        for attempt in range(10):
            with suppress(ui.UIErr):
                window = active_app.children.find_one(
                    AXRole="AXWindow",
                    AXSubrole="AXUnknown",
                    # AXTitle="Search, Suggestions available",
                    max_depth=0,
                )
                break
            actions.sleep("10ms")
        else:
            raise Exception("Unable to locate command search window")
        group = window.children.find_one(AXRole="AXGroup", max_depth=0)
        # jump over find and replace options
        menu_buttons = group.children.find(AXRole="AXMenuButton")[3:]
        for index, button in enumerate(menu_buttons):
            if button.AXEnabled == False:
                button = menu_buttons[index + 1]
                ctrl.mouse_move(*button.AXFrame.center)
                return
        raise Exception("No matching action")

    def office_document_actions():
        toolbar_group = document_window_toolbar_group()
        try:
            toolbar_group.children.find_one(
                AXRole="AXButton",
                AXIdentifier="CUIDocumentShellWindowAutosaveWidgetAutoID",
                max_depth=0,
            ).perform("AXPress")
        except ui.UIErr:
            raise Exception(f"Unable to locate document actions button")


mod.list("ribbon_items", desc="Ribbon tabs and controls (if visible)")
mod.list("ribbon_menus", desc="Ribbon menu buttons and menu items (if visible)")

RIBBON_ITEMS = {}


def matching_item(match):
    if item := RIBBON_ITEMS.get(match):
        return item

    for title, item in RIBBON_ITEMS.items():
        if match in title:
            return item

    message = f"No unique ribbon control title containing “{match}”"
    app.notify(body=message, title="Ribbon selection failed")
    raise Exception(message)


@mod.capture(rule="{user.ribbon_items}")
def ribbon_item(m) -> ui.Element:
    return matching_item(m.ribbon_items)


@mod.capture(rule="{user.ribbon_menus}")
def ribbon_menu(m) -> ui.Element:
    return matching_item(m.ribbon_menus)


# XXX Share with menu_select
RE_NON_ALPHA_OR_SPACE = re.compile(r"\s*[^A-Za-z\s]+\s*")
RE_INTERCAPS = re.compile(r"[a-z][A-Z]")


def spoken_forms(s):
    # XXX use user.vocabulary, or may never match
    has_non_alpha_or_space = RE_NON_ALPHA_OR_SPACE.search(s)
    if has_non_alpha_or_space or RE_INTERCAPS.search(s):
        spoken_forms = "\n".join(
            actions.user.create_spoken_forms(s, generate_subsequences=False)
        )
        if has_non_alpha_or_space:
            return f"""{spoken_forms}
{RE_NON_ALPHA_OR_SPACE.sub(" ", s.lower())}"""
        else:
            return spoken_forms
    return s.lower()


def element_title(e):
    title = None
    for attribute in ("AXTitle", "AXDescription"):
        try:
            if title := e.get(attribute):
                break
        except:
            pass
    if not title:
        title = e.get("AXIdentifier")  # last resort
        if title and title.startswith("_"):
            title = None

    return title


def enabled_items_with_role(element, role):
    return [
        item for item in element.children.find(AXRole=role, AXEnabled=True, max_depth=0)
    ]


def saved_item_selection_list(items, fallback=None):
    global RIBBON_ITEMS

    RIBBON_ITEMS = {}
    for item in items:
        spoken_title = ""
        if title := element_title(item):
            spoken_title = spoken_forms(title)
        elif fallback is not None:
            if element := fallback(item):
                if title := element_title(element):
                    spoken_title = spoken_forms(title)
        if spoken_title:
            RIBBON_ITEMS[spoken_title] = item

    return "\n".join(RIBBON_ITEMS.keys())


# XXX end share with menu_select


@ctx.action_class("user")
class UserActions:

    def office_mac_ribbon_item_select(ribbon_item):
        if ribbon_item.AXRole == "AXComboBox":
            ribbon_item.AXFocused = True
            return
        try:
            ribbon_item.perform("AXPress")
        except:  # XXX sometimes "fails" when it actually succeeds
            pass
        actions.user.help_refresh()

    def office_mac_ribbon_item_hover(ribbon_item):
        ctrl.mouse_move(*ribbon_item.AXFrame.center)

    def office_mac_ribbon_menu_select(ribbon_menu):
        if "AXShowMenu" in ribbon_menu.actions:
            ribbon_menu.perform("AXShowMenu")
            actions.user.help_refresh()
        else:
            actions.user.office_mac_ribbon_item_select(ribbon_menu)


def left_top(element, transpose=False):
    if frame := getattr(element, "AXFrame", None):
        return (frame.top, frame.left) if transpose else (frame.left, frame.top)
    else:
        return (0, 0)


def item_names(items, names=[], prefix="", across_then_down=False):
    elements = [
        (*left_top(element, across_then_down), f"{prefix}{element_title(element)}")
        for element in items
    ]
    elements.sort()
    if elements and names:
        names.append("")
    return names + [name for top, left, name in elements]


@ctx.dynamic_list("user.ribbon_items")
def ribbon_items(phrase: list[str]):
    tab_group = document_window_tab_group()
    items = enabled_items_with_role(tab_group, "AXRadioButton")
    if not phrase:
        names = item_names(items, prefix="• ")
        items = []

    try:
        tab = tab_group.children.find_one(AXRole="AXScrollArea", max_depth=0)
        for item in tab.children.find():
            if item.AXRole in (
                "AXButton",
                "AXCheckBox",
                "AXComboBox",
                "AXMenuButton",
                "AXRadioButton",
            ):
                items.append(item)
    except ui.UIErr as e:
        pass

    if not phrase:
        return item_names(items, names)

    return saved_item_selection_list(items)


@ctx.dynamic_list("user.ribbon_menus")
def ribbon_menus(phrase: list[str]):
    tab_group = document_window_tab_group()

    try:
        menu_window = ui.active_app().children.find_one(
            AXRole="AXWindow", AXSubrole="AXUnknown", max_depth=0
        )
        items = list(menu_window.children.find(AXRole="AXMenuButton"))
        if not phrase:
            names = [f"• {element_title(item)}" for item in items]
            items = []
    except ui.UIErr:
        names = []
        items = []

    try:
        tab = tab_group.children.find_one(AXRole="AXScrollArea", max_depth=0)
        items += list(tab.children.find(AXRole="AXMenuButton"))
    except ui.UIErr:
        return []

    if not phrase:
        return item_names(items, names)

    return saved_item_selection_list(items)
