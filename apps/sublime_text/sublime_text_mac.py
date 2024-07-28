from os.path import join
from subprocess import call

from talon import Context, Module, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
os: mac
app.bundle: com.sublimetext.4
"""


@ctx.action_class("app")
class AppActions:
    def tab_open():
        actions.key("cmd-n")

    def window_open():
        actions.key("cmd-shift-n")

    def window_close():
        actions.key("cmd-shift-w")


@ctx.action_class("code")
class CodeActions:
    def toggle_comment():
        actions.key("cmd-/")


@ctx.action_class("edit")
class EditActions:
    def jump_line(n: int):
        actions.key("ctrl-g")
        actions.insert(str(n))
        actions.key("enter")

    # more direct word/line processing - actions are in core,
    # but voice commands are enabled with tag(user.line_commands)
    def delete_line():
        actions.key("ctrl-shift-k")

    def line_clone():
        actions.key("cmd-shift-d")

    def line_swap_up():
        actions.key("cmd-ctrl-up")

    def line_swap_down():
        actions.key("cmd-ctrl-down")

    def indent_less():
        actions.key("cmd-[")

    def indent_more():
        actions.key("cmd-]")

    def select_word():
        actions.key("cmd-d")

    def select_line(n: int = None):
        actions.key("cmd-l")

    # user.find_and_replace
    def find(text: str):
        actions.key("cmd-f")
        actions.insert(text)


@ctx.action_class("user")
class UserActions:
    def sublime_text_find_in_project_files(text: str, files: str):
        actions.user.find_everywhere(text)
        actions.key("tab cmd-a")
        actions.insert("<project filters>," + files)
        actions.key("shift-tab")

    # user.find_and_replace
    def find_everywhere(text: str):
        actions.key("cmd-shift-f")
        actions.insert(text)

    def find_toggle_match_by_case():
        actions.key("cmd-alt-c")

    def find_toggle_match_by_word():
        actions.key("cmd-alt-w")

    def find_toggle_match_by_regex():
        actions.key("cmd-alt-r")

    def replace(text: str):
        actions.key("cmd-alt-f")
        actions.insert(text)

    def replace_confirm():
        actions.key("cmd-alt-e")

    def replace_confirm_all():
        actions.key("ctrl-alt-enter")

    replace_everywhere = find_everywhere

    def select_previous_occurrence(text: str):
        actions.key("cmd-i")
        actions.insert(text)
        actions.key("shift-enter")

    def select_next_occurrence(text: str):
        actions.key("cmd-i")
        actions.insert(text)
        actions.key("enter")

    # user.line_commands
    def delete_camel_left():
        actions.key("ctrl-backspace")

    def delete_camel_right():
        actions.key("ctrl-delete")

    def extend_camel_left():
        actions.key("ctrl-shift-left")

    def extend_camel_right():
        actions.key("ctrl-shift-right")

    def camel_left():
        actions.key("ctrl-left")

    def camel_right():
        actions.key("ctrl-right")

    # user.multiple_cursors
    def multi_cursor_add_above():
        actions.key("ctrl-shift-up")

    def multi_cursor_add_below():
        actions.key("ctrl-shift-down")

    def multi_cursor_add_to_line_ends():
        actions.key("cmd-shift-l")

    def multi_cursor_disable():
        actions.key("escape")

    def multi_cursor_enable():
        actions.skip()

    def multi_cursor_select_all_occurrences():
        actions.key("ctrl-cmd-g")

    def multi_cursor_select_fewer_occurrences():
        actions.key("cmd-u")

    def multi_cursor_select_more_occurrences():
        actions.key("cmd-d")

    # user.tabs
    def tab_jump(number: int):
        if number < 9:
            actions.key(f"cmd-{number}")


@ctx.action_class("win")
class WinActions:
    def filename():
        title = actions.win.title()
        result = title.split(" — ")[0]
        return result if "." in result else ""


@mod.action_class
class Actions:
    def subl(paths: list[str]):
        """Open the specified paths in Sublime Text"""
        sublime_text = actions.user.launch_or_focus_bundle("com.sublimetext.4")
        subl_path = join(sublime_text.path, "Contents/SharedSupport/bin/subl")
        call([subl_path, "--"] + paths)

    def sublime_text_find_in_project_files(text: str, files: str):
        """Find text in the specified project files"""
