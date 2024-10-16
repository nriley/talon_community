from talon import Context, Module, actions, clip, ui

try:
    from appscript.reference import CommandError
except ImportError:
    pass

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


@ctx.action_class("edit")
class EditActions:
    def find(text: str = None):
        if text:
            clip.set_text(text, mode="find")
        actions.key("cmd-f enter")

    def zoom_in():
        actions.key("cmd-ctrl-+")

    def zoom_out():
        actions.key("cmd-ctrl--")

    def zoom_reset():
        actions.key("cmd-ctrl-0")


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
        try:
            if not (records := browser_window.selected_records(timeout=0.1)):
                if not (records := browser_window.current_records(timeout=0.1)):
                    return None
        except CommandError:
            return None

        # XXX work around https://github.com/talonvoice/appscript/issues/1
        from urllib.parse import unquote

        return unquote(records[0].file().path)

    def file_manager_show_properties():
        actions.key("cmd-i")

    def file_manager_new_folder(name: str):
        actions.key("cmd-shift-n")
        actions.sleep("500ms")
        actions.insert(name)

    def find_everywhere(text: str):
        actions.key("cmd-alt-f")
        actions.user.paste(text)

    def zoom_to_fit():
        actions.key("cmd-shift-ctrl--")


@mod.action_class
class Actions:
    def eaglefiler_select_first_displayed_record():
        """Select the first displayed record in the front message viewer in EagleFiler."""
