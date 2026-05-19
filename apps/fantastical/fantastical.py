from contextlib import suppress

from talon import Context, Module, actions, ui

ctx = Context()
mod = Module()

ctx.matches = r"""
os: mac
"""

mod.apps.fantastical = """
os: mac
and app.bundle: 85C27NK92C.com.flexibits.fantastical2.mac.helper
os: mac
and app.bundle: com.flexibits.fantastical2.mac
"""


def fantastical_calendar_window():
    window = ui.active_window()
    if not window or window.element.get("AXSubrole", None) != "AXStandardWindow":
        return None
    return window


def fantastical_notifications():
    if not (window := fantastical_calendar_window()):
        return None

    if window.element.get("AXIdentifier") == "mini window":
        buttons = window.children.find(
            AXRole="AXButton", AXIdentifier="notifications", max_depth=0
        )
    else:
        buttons = (
            window.children.find_one(AXRole="AXSplitGroup", max_depth=0)
            .children.find_one(AXRole="AXToolbar", max_depth=0)
            .children.find(AXRole="AXButton", AXIdentifier="notifications", max_depth=0)
        )

    if not buttons:
        return None

    return buttons[0]


@ctx.action_class("user")
class UserActions:
    def fantastical_parse(text: str):
        ui.apps(bundle="com.flexibits.fantastical2.mac")[0].appscript().parse_sentence(
            text
        )

    def fantastical_show_mini_calendar():
        import webbrowser

        webbrowser.open("x-fantastical3://show/mini")

    def fantastical_show_calendar():
        import webbrowser

        webbrowser.open("x-fantastical3://show/calendar")

    def fantastical_show_notifications():
        if not (notifications := fantastical_notifications()):
            return

        with suppress(Exception):
            # raises talon.mac.ui.ActionFailed even when it works
            notifications.perform("AXPress")

        for _attempt in range(10):
            actions.sleep("50ms")
            try:
                if notifications.children:
                    break
            except AttributeError:  # XXX Talon bug?
                pass
        else:
            return

        notifications.children[0].children.find_one(AXRole="AXRow").AXSelected = True

    def fantastical_clear_all_notifications():
        if not (notifications := fantastical_notifications()):
            return

        try:
            if notifications.children:
                pass
        except AttributeError:
            actions.user.fantastical_show_notifications()
            try:
                if notifications.children:
                    pass
            except AttributeError:
                return

        try:
            button = notifications.children[0].children.find_one(AXRole="AXMenuButton")
            button.perform("AXPress")
        except ui.UIErr:
            actions.key("cmd-enter")

        for _attempt in range(10):
            actions.sleep("50ms")
            try:
                menu = ui.active_menu()
                if menu.parent == button:
                    break
            except AttributeError:  # XXX Talon bug?
                pass
        else:
            return

        clear_all = menu.children.find_one(
            AXRole="AXMenuItem", AXIdentifier="confirmAllNotifications"
        )
        clear_all.perform("AXPress")

    def fantastical_select_calendar_set(text):
        if not (window := fantastical_calendar_window()):
            return

        try:
            split = window.children.find_one(AXRole="AXSplitGroup", max_depth=0)
            if split.AXSplitters[0].AXValue == 0:
                actions.user.menu_select("View|Show Sidebar")
                for _attempt in range(10):
                    if split.AXSplitters[0].AXValue > 0:
                        break
                    actions.sleep("50ms")
            parent = split.children.find_one(
                AXRole="AXGroup", AXDescription="sidebar", max_depth=0
            )
        except:
            parent = window

        parent.children.find_one(
            AXRole="AXPopUpButton", AXDescription="calendar set", max_depth=0
        ).perform("AXPress")

        if text:
            actions.key("home")
            actions.insert(text)

    def fantastical_show_menu():
        fantastical_helper = ui.apps(
            bundle="85C27NK92C.com.flexibits.fantastical2.mac.helper"
        )[0]
        menu_extra = fantastical_helper.children.find_one(
            AXRole="AXMenuBarItem", AXSubrole="AXMenuExtra", max_depth=1
        )
        with suppress(ui.ActionFailed):
            menu_extra.perform("AXPress")

        for _attempt in range(10):
            try:
                menu_extra.children.find_one(
                    AXRole="AXMenuItem", AXIdentifier="conferenceMenuItemSelected:"
                )
                break
            except ui.UIErr:
                pass
            actions.sleep("10ms")
        else:
            raise Exception("Can't find conference menu item")


@mod.action_class
class Actions:
    def fantastical_parse(text: str):
        """Parses text in Fantastical"""

    def fantastical_select_calendar_set(text: str):
        """Select a calendar set in Fantastical"""

    def fantastical_show_mini_calendar():
        """Shows the mini calendar popover"""

    def fantastical_show_calendar():
        """Shows the calendar window"""

    def fantastical_show_notifications():
        """Shows the notifications/invitations popover"""

    def fantastical_clear_all_notifications():
        """Clears all contents from the notifications/invitations popover"""

    def fantastical_show_menu():
        """Show the Fantastical menu"""
