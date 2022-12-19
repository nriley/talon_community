from talon import Context, Module, actions, app, ui

ctx = Context()
mod = Module()

mod.tag("homerow_search")


@ctx.action_class("user")
class UserActions:
    def homerow_pick(label: str):
        actions.insert(label.upper())
        actions.key("enter")
        complete_homerow_search()


@mod.action_class
class Actions:
    def homerow_pick(label: str):
        """Pick a label in Homerow"""


def complete_homerow_search():
    ctx.tags = []
    ui.unregister("element_focus", element_focus)


def element_focus(element):
    complete_homerow_search()


def win_open(win):
    if win.app.bundle != "com.dexterleng.Homerow":
        return
    if win.title != "Homerow Search Bar":
        return
    if len(ctx.tags) == 0:
        ctx.tags = ["user.homerow_search"]
        ui.register("element_focus", element_focus)


if app.platform == "mac":
    app.register("ready", lambda: ui.register("win_open", win_open))
