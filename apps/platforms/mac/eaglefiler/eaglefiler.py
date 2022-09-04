from appscript.reference import CommandError
from talon import Context, Module, actions, ui

ctx = Context()
mod = Module()

mod.apps.eaglefiler = r"""
os: mac
and app.bundle: com.c-command.EagleFiler
"""

ctx.matches = r"""
app: eaglefiler
"""


def eaglefiler_front_browser_window():
    ef = ui.apps(bundle="com.c-command.EagleFiler")[0]
    return ef.appscript().browser_windows[1]


@ctx.action_class("user")
class UserActions:
    def eaglefiler_select_first_displayed_record():
        browser_window = eaglefiler_front_browser_window()
        try:
            if not (displayed_records := browser_window.displayed_records()):
                return None
        except CommandError:
            return None

        browser_window.selected_records.set(displayed_records[0])

    def file_manager_open_parent():
        actions.key("cmd-up")

    def file_manager_current_path():
        browser_window = eaglefiler_front_browser_window()
        selected_records = browser_window.selected_records()
        if not selected_records:
            return None
        return selected_records[0].file().path

    def file_manager_show_properties():
        actions.key("cmd-i")

    def file_manager_new_folder(name: str):
        actions.key("cmd-shift-n")
        actions.sleep("500ms")
        actions.insert(name)


@mod.action_class
class Actions:
    def eaglefiler_select_first_displayed_record():
        """Select the first displayed record in the front message viewer in EagleFiler."""
