from talon import Context, Module, actions, app, ui

mod = Module()
ctx = Context()
ctx_mac = Context()

mod.apps.rstudio = r"""
os: mac
and app.bundle: com.rstudio.desktop
os: windows
and app.exe: rstudio.exe
"""

ctx.matches = r"""
app: rstudio
"""

ctx_mac.matches = r"""
os: mac
app: rstudio
"""


@ctx_mac.action_class("app")
class AppActions:
    def tab_open():
        actions.key("cmd-shift-n")

    def tab_next():
        actions.key("ctrl-f12")

    def tab_previous():
        actions.key("ctrl-f11")


@ctx.action_class("code")
class CodeActions:
    def language():
        # Default to R language.
        # Could use ui.register to detect focusing a document/console tab (on Mac at least)
        if next_language := actions.next():
            return next_language
        return "r"


@ctx_mac.action_class("code")
class CodeActions:
    def toggle_comment():
        actions.key("cmd-shift-c")


@ctx_mac.action_class("edit")
class EditActions:
    # user.line_commands
    def jump_line(n):
        actions.key("cmd-shift-alt-g")
        actions.sleep("200ms")
        actions.insert(n)
        actions.key("enter")
        actions.edit.line_start()

    def line_clone():
        actions.key("cmd-alt-down")

    def line_swap_up():
        actions.key("alt-up")

    def line_swap_down():
        actions.key("alt-down")

    # user.find_and_replace
    def find(text: str = None):
        actions.key("cmd-f")
        if text:
            actions.key("cmd-a")
            actions.user.paste(text)


@ctx_mac.action_class("user")
class UserActions:
    # user.find_and_replace
    def find_everywhere(text: str):
        actions.key("cmd-shift-f")

    def find_toggle_match_by_case():
        actions.edit.find("")
        actions.key("tab:8 space")

    def find_toggle_match_by_word():
        actions.edit.find("")
        actions.key("tab:9 space")

    def find_toggle_match_by_regex():
        actions.edit.find("")
        actions.key("tab:10 space")

    def replace(text: str):
        actions.user.find(text)

    replace_everywhere = find_everywhere

    def replace_confirm():
        actions.key("cmd-shift-j")

    def replace_confirm_all():
        actions.edit.find("")
        actions.key("tab:6 space")

    def select_previous_occurrence(text: str):
        # Can't entirely suppress the find pane but at least hide it
        actions.edit.find(text)
        actions.edit.find_previous()
        actions.key("esc")

    def select_next_occurrence(text: str):
        # Can't entirely suppress the find pane but at least hide it
        actions.edit.find(text)
        actions.edit.find_next()
        actions.key("esc")

    # user.multiple_cursors
    def multi_cursor_disable():
        actions.key("esc")

    def multi_cursor_add_above():
        actions.key("ctrl-alt-up")

    def multi_cursor_add_below():
        actions.key("ctrl-alt-down")

    def multi_cursor_add_to_line_ends():
        actions.key("ctrl-alt-a")

    # user.tabs
    def tab_final():
        actions.key("ctrl-shift-f12")
