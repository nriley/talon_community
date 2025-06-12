from talon import Context, Module, actions, app, ui

ctx = Context()
mod = Module()

ctx.matches = r"""
app: excel_win
"""


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.key("alt-w n")


@ctx.action_class("user")
class UserActions:
    def excel_save_as_format(format: str):
        actions.user.office_win_ribbon_select("fa")
        actions.sleep("500ms")
        actions.insert("yc")

        document_window = ui.active_window().element

        for attempt in range(10):
            try:
                el = ui.active_window().element
                if el.control_type == "Menu" and el.name == "Save as type":
                    file_format_menu = el
                    break
            except ui.UIErr:
                actions.sleep("100ms")
        else:
            app.notify(body="Did not find save as type menu as expected", title="Excel")
            return

        # Menu is a separate window but does not contain the items;
        # go back to the document window for that
        file_format_item = document_window.find_one(
            control_type="ListItem", name=format
        )
        file_format_item.invoke_pattern.invoke()
