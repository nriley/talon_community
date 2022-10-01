from talon import Context, Module, actions

ctx = Context()
mod = Module()

ctx.matches = r"""
os: windows
and app.exe: OUTLOOK.EXE
"""


@ctx.action_class("user")
class UserActions:
    def find(text: str):
        actions.key("f4")
        if text:
            actions.insert(text)

    def find_next():
        actions.key("f4 alt-f")

    def find_previous():
        pass

    def find_everywhere(text: str):
        actions.key("ctrl-e")
        if text:
            actions.insert(text)

    def find_toggle_match_by_case():
        actions.key("alt-m alt-h")

    def find_toggle_match_by_word():
        actions.key("alt-m alt-y")

    def find_toggle_match_by_regex():
        pass

    def replace(text: str):
        actions.key("ctrl-h")
        if text:
            actions.insert(text)

    replace_everywhere = replace

    def replace_confirm():
        pass

    def replace_confirm_all():
        pass

    def select_previous_occurrence(text: str):
        pass

    def select_next_occurrence(text: str):
        actions.edit.find(text)
        actions.edit.find_next()
        actions.key("esc")
