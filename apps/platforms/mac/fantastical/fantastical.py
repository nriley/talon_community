from talon import Context, Module

ctx = Context()
mod = Module()

ctx.matches = r"""
os: mac
"""


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

    def fantastical_select_calendar_set(text):
        window = ui.active_window()
        if not window or window.element.AXSubrole != "AXStandardWindow":
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
