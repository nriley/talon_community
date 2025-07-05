import re
from collections.abc import Callable
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
    return (
        actions.user.office_mac_document_window()
        .children.find_one(AXRole="AXToolbar", max_depth=0)
        .children.find_one(AXRole="AXGroup", max_depth=0)
    )


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

    def office_tell_me():
        try:  # OneNote only as of 6/9/2025
            document_window_tab_group().children.find_one(
                AXRole="AXButton", AXTitle="Tell me", max_depth=0
            ).perform("AXPress")
            return
        except ui.UIErr:
            pass

        try:
            toolbar_group = document_window_toolbar_group()
        except ui.UIErr:
            raise Exception(f"Unable to locate window toolbar")
        try:
            toolbar_group.children.find_one(
                AXRole="AXTextField", AXSubrole="AXSearchField", max_depth=0
            ).AXFocused = True
        except ui.UIErr:
            toolbar_buttons = toolbar_group.children.find(
                AXRole="AXButton", AXRoleDescription="button"
            )
            for button in toolbar_buttons:
                # XXX could use frame, otherwise no way to distinguish, so English-only for now
                if button.AXTitle.startswith("Search ("):
                    button.perform("AXPress")
                    return
            raise Exception(f"Unable to locate Search button")

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

    def office_mac_ribbon_item_select(ribbon_item: ui.Element):
        if ribbon_item.AXRole == "AXComboBox":
            ribbon_item.AXFocused = True
            return
        try:
            ribbon_item.perform("AXPress")
        except:  # XXX sometimes "fails" when it actually succeeds
            pass

    def office_mac_ribbon_item_hover(ribbon_item: ui.Element):
        ctrl.mouse_move(*ribbon_item.AXFrame.center)


@ctx.dynamic_list("user.ribbon_items")
def ribbon_items(phrase: list[str]):
    tab_group = document_window_tab_group()
    items = enabled_items_with_role(tab_group, "AXRadioButton")

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

    return saved_item_selection_list(items)
