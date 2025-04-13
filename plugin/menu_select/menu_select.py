import os
import re

from talon import Context, Module, actions, app, ctrl, ui

mod = Module()
ctx = Context()

ctx.matches = r"""
os: mac
"""

mod.list("menu_items", desc="Active menu items and/or menu bar items")
mod.list("menu_extras", desc="Menu extras' menu bar items")

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


@mod.capture(rule="{user.menu_extras}")
def menu_extra(m) -> ui.Element:
    return matching_item(m.menu_extras)


RE_NON_ALPHA_OR_SPACE = re.compile(r"\s*[^A-Za-z\s]+\s*")


def spoken_forms(s):
    # XXX use user.vocabulary, or may never match
    if RE_NON_ALPHA_OR_SPACE.search(s):
        spoken_forms = "\n".join(
            actions.user.create_spoken_forms(s, generate_subsequences=False)
        )
        return f"""{spoken_forms}
{RE_NON_ALPHA_OR_SPACE.sub(" ", s.lower())}"""
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
    global MENU_ITEMS

    MENU_ITEMS = {}
    for item in items:
        spoken_title = ""
        if title := element_title(item):
            spoken_title = spoken_forms(title)
        if fallback is not None:
            if element := fallback(item):
                if title := element_title(element):
                    if spoken_title:
                        spoken_title = f"{spoken_title}\n{spoken_forms(title)}"
                    else:
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


@ctx.action_class("user")
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
                return
            except:
                pass

        new_var = 1
        ctrl.mouse_click(new_var)

    def menu_item_select(menu_item: ui.Element):
        try:
            menu_item.perform("AXPress")
        except:  # XXX sometimes "fails" when it actually succeeds
            pass

    def menu_item_hover(menu_item: ui.Element):
        ctrl.mouse_move(*menu_item.AXFrame.center)


@ctx.dynamic_list("user.menu_items")
def menu_items(phrase: list[str]):
    items = []

    if menu := ui.active_menu():
        items = enabled_items_with_role(menu, "AXMenuItem")
        while True:
            parent = menu.AXParent
            if (parent_role := parent.AXRole) not in ("AXMenuBarItem", "AXMenuItem"):
                break
            menu = parent.AXParent
            items += enabled_items_with_role(menu, parent_role)
    else:
        items = enabled_items_with_role(
            ui.active_app().element.AXMenuBar, "AXMenuBarItem"
        )

    return saved_item_selection_list(items)


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


@ctx.dynamic_list("user.menu_extras")
def menu_extras(phrase: list[str]):
    items = []
    singletons = []  # can't use set as Element is unhashable
    # XXX some menus start slightly off the top of the screen; if still over-filters, consider matching x only
    screen_rect = display_area().inset(-1)

    talon_pid = os.getpid()
    for app in ui.apps():
        try:
            if app.pid == talon_pid:
                continue  # XXX can pop up menu extra but can't select from it

            if "/XPCServices/" in app.exe:
                continue  # XXX hangs; can we filter these out more cleanly?

            if menu_bar := app.element.AXExtrasMenuBar:
                if not screen_rect.contains(menu_bar.AXPosition):
                    continue

                app_items = enabled_items_with_role(menu_bar, "AXMenuBarItem")
                if len(app_items) == 1:
                    singletons.append(app_items[0])
                items += app_items
        except:
            pass

    def fallback(item):
        if item in singletons:
            return item.AXTopLevelUIElement.AXParent

    return saved_item_selection_list(items, fallback)
