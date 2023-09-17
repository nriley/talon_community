from talon import Context, Module, actions, app, ui

ctx = Context()
mod = Module()

mod.tag("homerow_search")

search_again = False


@ctx.action_class("user")
class UserActions:
    def homerow_search(text: str):
        try:
            if (
                len(ctx.tags) > 0
                and (focused_element := ui.focused_element())
                and win_is_homerow_search_bar(focused_element.window)
            ):
                focused_element.AXValue = text.lower()
                return
        except ui.UIErr:
            # focused_element.window sometimes raises a UIErr
            # (when the Homerow search window is not visible)
            pass

        actions.key("ctrl-alt-shift-h")
        for attempt in range(10):
            actions.sleep("50ms")
            try:
                focused_element = ui.focused_element()
                if win_is_homerow_search_bar(focused_element.window):
                    focused_element.AXValue = text.lower()
                    return
            except:
                pass

    def homerow_pick(label: str, again: bool):
        global search_again

        search_again = again
        actions.insert(label.upper())
        actions.key("enter")
        complete_homerow_search()


@mod.action_class
class Actions:
    def homerow_search(text: str):
        """Search in Homerow"""

    def homerow_pick(label: str, again: bool):
        """Pick a label in Homerow, optionally continuing to search"""


def win_close(win):
    if win_is_homerow_search_bar(win):
        complete_homerow_search()


def complete_homerow_search():
    global search_again

    ctx.tags = []
    ui.unregister("win_close", win_close)
    if search_again:
        search_again = False
        actions.user.homerow_search("")


def win_is_homerow_search_bar(win):
    return (
        win.app.bundle == "com.dexterleng.Homerow" and win.title == "Homerow Search Bar"
    )


def win_open(win):
    if not win_is_homerow_search_bar(win):
        return
    if len(ctx.tags) == 0:
        ctx.tags = ["user.homerow_search"]
        ui.register("win_close", win_close)


if app.platform == "mac":
    app.register("ready", lambda: ui.register("win_open", win_open))
