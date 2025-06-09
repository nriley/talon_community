import os
import re

from talon import Context, Module, actions, app, ctrl, imgui, ui

mod = Module()
ctx_mac = Context()
ctx_win_citrix = Context()

ctx_mac.matches = r"""
os: mac
"""

ctx_win_citrix.matches = r"""
os: windows
os: mac
and app: citrix_viewer_mac
"""


mod.list("menu_items", desc="Active menu items and/or menu bar items")
mod.list("contextual_menu_items", "Active contextual menu items")
mod.list("status_menus", desc="Status menus' menu bar items")

MENU_ITEMS = {}


def matching_item(match):
    if item := MENU_ITEMS.get(match):
        return item

    for title, item in MENU_ITEMS.items():
        if match in title:
            return item

    message = f"No unique menu item title containing “{match}”"
    app.notify(body=message, title="Menu selection failed")
    raise Exception(message)


@mod.capture(rule="{user.menu_items}")
def menu_item(m) -> ui.Element:
    return matching_item(m.menu_items)


@mod.capture(rule="{user.contextual_menu_items}")
def contextual_menu_item(m) -> ui.Element:
    return matching_item(m.contextual_menu_items)


@mod.capture(rule="{user.status_menus}")
def status_menu(m) -> ui.Element:
    return matching_item(m.status_menus)


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


def item_titles(items, fallback=None):
    for item in items:
        if title := element_title(item):
            yield title
        elif fallback is not None:
            if element := fallback(item):
                if title := element_title(element):
                    yield title


def saved_item_selection_list(items, fallback=None):
    global MENU_ITEMS

    MENU_ITEMS = {}
    for item in items:
        spoken_title = ""
        if title := element_title(item):
            spoken_title = spoken_forms(title)
        elif fallback is not None:
            if element := fallback(item):
                if title := element_title(element):
                    spoken_title = spoken_forms(title)
        if spoken_title:
            MENU_ITEMS[spoken_title] = item

    return "\n".join(MENU_ITEMS.keys())


@mod.action_class
class Actions:
    def contextual_menu_open():
        """Open contextual menu"""

    def menu_item_select(menu_item: ui.Element):
        """Select the specified menu item"""

    def menu_item_hover(menu_item: ui.Element):
        """Move the mouse pointer to the specified menu item"""

    def status_menus_hide() -> bool:
        """Hide display of titles of status menus (returns whether they were displayed)"""

    def status_menus_toggle():
        """Display or hide titles of status menus"""


STATUS_MENU_TITLES = []


@imgui.open()
def gui_extras(gui: imgui.GUI):
    global STATUS_MENU_TITLES

    gui.text("Status menus (left to right)")
    gui.text("Say “status [hover | touch] <name>”")
    gui.line()
    for title in STATUS_MENU_TITLES:
        gui.text(title)
    gui.spacer()
    if gui.button("Close (say “status menus”)"):
        actions.user.status_menus_toggle()


@ctx_mac.action_class("user")
class UserActions:
    def contextual_menu_open():
        if ui.active_menu():
            return

        actions.key("menu")
        actions.sleep("50ms")
        if ui.active_menu():
            return

        if (element := ui.focused_element()) is not None:
            try:
                element.perform("AXShowMenu")
                actions.sleep("50ms")
                if ui.active_menu():
                    return
            except:
                pass

        ctrl.mouse_click(1)

        for attempt in range(10):
            actions.sleep("50ms")
            if ui.active_menu() is not None:
                return

        raise Exception("Unable to pop up contextual menu")

    def menu_item_select(menu_item: ui.Element):
        try:
            menu_item.perform("AXPress")
        except:  # XXX sometimes "fails" when it actually succeeds
            pass

    def menu_item_hover(menu_item: ui.Element):
        ctrl.mouse_move(*menu_item.AXFrame.center)

    def status_menus_hide() -> bool:
        global STATUS_MENU_TITLES

        if not gui_extras.showing:
            return False

        gui_extras.hide()
        STATUS_MENU_TITLES = []
        return True

    def status_menus_toggle():
        global STATUS_MENU_TITLES

        if actions.user.status_menus_hide():
            return

        items, fallback = status_menu_items_fallback()
        items.sort(key=lambda i: i.AXPosition.x)
        STATUS_MENU_TITLES = list(item_titles(items, fallback))

        cc = ui.apps(bundle="com.apple.controlcenter")[0]
        menubar = cc.element.children.find_one(AXRole="AXMenuBar", max_depth=0)
        frame = menubar.AXFrame

        gui_extras.x = frame.left - 100
        gui_extras.y = frame.top
        gui_extras.show()


@ctx_win_citrix.action_class("user")
class UserActions:
    def contextual_menu_open():
        actions.key("shift-f10")


@ctx_mac.dynamic_list("user.menu_items")
def menu_items(phrase: list[str]):
    items = []

    if menu := ui.active_menu():
        items = enabled_items_with_role(menu, "AXMenuItem")
        while parent := getattr(menu, "AXParent", None):
            if (parent_role := parent.AXRole) not in ("AXMenuBarItem", "AXMenuItem"):
                break
            menu = parent.AXParent
            items += enabled_items_with_role(menu, parent_role)
    else:
        items = enabled_items_with_role(
            ui.active_app().element.AXMenuBar, "AXMenuBarItem"
        )

    return saved_item_selection_list(items)


@ctx_mac.dynamic_list("user.contextual_menu_items")
def contextual_menu_items(phrase: list[str]):
    actions.user.contextual_menu_open()
    return menu_items(phrase)


def display_area():
    screen_rect = ui.Rect(0, 0, 0, 0)

    for screen in ui.screens():
        if screen.rect.left < screen_rect.left:
            screen_rect.left = screen.rect.left
        if screen.rect.right > screen_rect.right:
            screen_rect.right = screen.rect.right
        if screen.rect.top < screen_rect.top:
            screen_rect.top = screen.rect.top
        if screen.rect.bot > screen_rect.bot:
            screen_rect.bot = screen.rect.bot

    return screen_rect


def status_menu_items_fallback():
    items = []
    singletons = []  # can't use set as Element is unhashable
    # XXX some menus start slightly off the top of the screen; if still over-filters, consider matching x only
    screen_rect = display_area().inset(-1)

    talon_pid = os.getpid()
    for app in ui.apps():
        if app.pid == talon_pid:
            continue  # XXX can pop up menu extra but can't select from it

        if "/XPCServices/" in app.exe:
            continue  # XXX hangs; can we filter these out more cleanly?

        if menu_bar := getattr(app.element, "AXExtrasMenuBar", None):
            if (position := getattr(menu_bar, "AXPosition", None)) is None:
                continue

            if not screen_rect.contains(position):
                continue

            app_items = enabled_items_with_role(menu_bar, "AXMenuBarItem")
            if len(app_items) == 1:
                singletons.append(app_items[0])
            items += app_items

    def fallback(item):
        if item in singletons:
            return item.AXTopLevelUIElement.AXParent

    return items, fallback


@ctx_mac.dynamic_list("user.status_menus")
def status_menus(phrase: list[str]):
    return saved_item_selection_list(*status_menu_items_fallback())
