from pathlib import Path
from subprocess import call

from talon import Context, actions, app, ui

ctx = Context()
ctx.matches = r"""
os: windows
and app.exe: sublime_text.exe
"""


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.key("ctrl-shift-n")

    def window_close():
        actions.key("ctrl-shift-w")

    def tab_open():
        actions.key("ctrl-n")

    def tab_next():
        actions.key("ctrl-pagedown")

    def tab_previous():
        actions.key("ctrl-pageup")


@ctx.action_class("code")
class CodeActions:
    def toggle_comment():
        actions.key("ctrl-/")


@ctx.action_class("edit")
class EditActions:
    # more direct word/line processing - actions are in core,
    # but voice commands are enabled with tag(user.line_commands)
    def delete_line():
        actions.key("ctrl-shift-k")

    def line_clone():
        actions.key("ctrl-shift-d")

    def line_swap_up():
        actions.key("ctrl-shift-up")

    def line_swap_down():
        actions.key("ctrl-shift-down")

    def select_word():
        actions.key("ctrl-d")

    def select_line(n: int = None):
        actions.key("ctrl-l")

    def jump_line(n: int):
        actions.key("ctrl-g")
        actions.insert(str(n))
        actions.key("enter")


@ctx.action_class("user")
class UserActions:
    def sublime_text_find_in_project_files(text: str, files: str):
        actions.user.find_everywhere(text)
        actions.key("tab ctrl-a")
        actions.insert("<project filters>," + files)
        actions.key("shift-tab")

    # user.find_and_replace
    def find_toggle_match_by_case():
        actions.key("alt-c")

    def find_toggle_match_by_word():
        actions.key("alt-w")

    def find_toggle_match_by_regex():
        actions.key("alt-r")

    def find_next():
        actions.key("f3")

    def find_previous():
        actions.key("shift-f3")

    def replace_confirm():
        actions.key("ctrl-shift-h")

    def replace_confirm_all():
        actions.key("ctrl-alt-enter")

    # user.line_commands
    def extend_camel_left():
        actions.key("alt-shift-left")

    def extend_camel_right():
        actions.key("alt-shift-right")

    def camel_left():
        actions.key("alt-left")

    def camel_right():
        actions.key("alt-right")

    # user.multiple_cursors
    def multi_cursor_add_above():
        actions.key("ctrl-alt-up")

    def multi_cursor_add_below():
        actions.key("ctrl-alt-down")

    def multi_cursor_add_to_line_ends():
        actions.key("ctrl-shift-l")

    def multi_cursor_disable():
        actions.key("escape")

    def multi_cursor_enable():
        actions.skip()

    def multi_cursor_select_all_occurrences():
        actions.key("alt-f3")

    def multi_cursor_select_fewer_occurrences():
        actions.key("ctrl-u")

    def multi_cursor_select_more_occurrences():
        actions.key("ctrl-d")

    def find(text: str):
        actions.key("ctrl-f")
        actions.insert(text)

    def find_everywhere(text: str):
        actions.key("ctrl-shift-f")
        actions.insert(text)

    def replace(text: str):
        actions.key("ctrl-h")
        actions.insert(text)

    replace_everywhere = find_everywhere

    def select_previous_occurrence(text: str):
        actions.key("ctrl-i")
        actions.insert(text)
        actions.key("shift-enter")

    def select_next_occurrence(text: str):
        actions.key("ctrl-i")
        actions.insert(text)
        actions.key("enter")


@ctx.action_class("win")
class WinActions:
    def filename():
        title = actions.win.title()
        result = title.rsplit(" - Sublime Text", 1)[0]
        result = result.rsplit(" (", 1)[0]
        result = result.rsplit(" •", 1)[0]
        return result if "." in result else ""


ctx_global = Context()

ctx_global.matches = r"""
os: windows
"""


@ctx_global.action_class("user")
class Actions:
    def subl(paths: list[str]):
        sublime_text = ui.apps(name="Sublime Text")
        if not sublime_text:
            app.notify("Sublime Text is not running.")
            return
        else:
            sublime_text = sublime_text[0]
        subl_path = str(Path(sublime_text.exe).parents[0] / "subl.exe")
        call([subl_path, "--"] + paths)
