from talon import Context, Module, actions, ui

ctx = Context()
mod = Module()

ctx.matches = r"""
os: mac
"""


def fantastical_calendar_window():
    window = ui.active_window()
    if not window or window.element.AXSubrole != "AXStandardWindow":
        return None
    return window


@ctx.action_class("user")
class UserActions:
    def fantastical_parse(text: str):
        ui.apps(bundle="com.flexibits.fantastical2.mac")[0].appscript().parse_sentence(
            text
        )

    def fantastical_show_mini_calendar():
        import webbrowser

        webbrowser.open(f"x-fantastical3://show/mini")

    def fantastical_show_calendar():
        import webbrowser

        webbrowser.open(f"x-fantastical3://show/calendar")

    def fantastical_show_notifications():
        if not (window := fantastical_calendar_window()):
            return

        if window.element.get("AXIdentifier") == "mini window":
            buttons = window.children.find(
                AXRole="AXButton", AXIdentifier="notifications", max_depth=0
            )
        else:
            buttons = (
                window.children.find_one(AXRole="AXSplitGroup", max_depth=0)
                .children.find_one(AXRole="AXToolbar", max_depth=0)
                .children.find(
                    AXRole="AXButton", AXIdentifier="notifications", max_depth=0
                )
            )

        if not buttons:
            return

        buttons[0].perform("AXPress")

        for attempt in range(10):
            actions.sleep("50ms")
            try:
                if buttons[0].children:
                    break
            except AttributeError:  # XXX Talon bug?
                pass
        else:
            return

        buttons[0].children[0].children.find_one(AXRole="AXRow").AXSelected = True

    def fantastical_select_calendar_set(text):
        if not (window := fantastical_calendar_window()):
            return

        try:
            split = window.children.find_one(AXRole="AXSplitGroup", max_depth=0)
            if split.AXSplitters[0].AXValue == 0:
                actions.user.menu_select("View|Show Sidebar")
                for attempt in range(10):
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
        try:
            menu_extra.perform("AXPress")
        except:
            pass  # XXX generates talon.mac.ui.ActionFailed

        for attempt in range(10):
            try:
                join_item = menu_extra.children.find_one(
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

    def fantastical_show_menu():
        """Show the Fantastical menu"""
