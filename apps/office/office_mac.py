import re

from talon import Context, Module, actions, ctrl, ui

mod = Module()
ctx = Context()

mod.apps.excel_mac = """
os: mac
and app.bundle: com.microsoft.Excel
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
app: powerpoint_mac
app: word_mac
"""

ctx.matches = """
app: office_mac
"""


def document_window():
    return ui.active_app().children.find_one(
        AXRole="AXWindow", AXSubrole="AXStandardWindow", max_depth=0
    )


def document_window_toolbar_group():
    return (
        document_window()
        .children.find_one(AXRole="AXToolbar", max_depth=0)
        .children.find_one(AXRole="AXGroup", max_depth=0)
    )


def document_window_tab_group():
    return document_window().children.find_one(AXRole="AXTabGroup", max_depth=0)


@mod.action_class
class Actions:
    def office_document_actions():
        """Opens the document actions popover"""

    def ribbon_item_select(ribbon_item: ui.Element):
        """Select the specified ribbon control"""

    def ribbon_item_hover(ribbon_item: ui.Element):
        """Move the mouse pointer to the specified ribbon control"""


@ctx.action_class("user")
class UserActions:
    def office_tell_me():
        toolbar_group = document_window_toolbar_group()
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

    def ribbon_item_select(ribbon_item: ui.Element):
        try:
            ribbon_item.perform("AXPress")
        except:  # XXX sometimes "fails" when it actually succeeds
            pass

    def ribbon_item_hover(ribbon_item: ui.Element):
        ctrl.mouse_move(*ribbon_item.AXFrame.center)


@ctx.dynamic_list("user.ribbon_items")
def ribbon_items(phrase: list[str]):
    tab_group = document_window_tab_group()
    items = enabled_items_with_role(tab_group, "AXRadioButton")

    tab = tab_group.children.find_one(AXRole="AXScrollArea", max_depth=0)
    for item in tab.children.find():
        if item.AXRole in (
            "AXButton",
            "AXCheckBox",
            "AXComboBox",
            "AXMenuButton",
        ):
            items.append(item)

    return saved_item_selection_list(items)
