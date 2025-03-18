from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.apps.outlook_mail_win = r"""
app: outlook_win
and not win.title: /^(Calendar|Contacts|To Do) -/
"""

mod.apps.outlook_calendar_win = r"""
app: outlook_win
win.title: /^Calendar -/
"""

ctx.matches = """
app: outlook_win
"""


@ctx.action_class("edit")
class EditActions:
    def find(text: str = None):
        actions.key("f4")
        if text:
            actions.insert(text)

    def find_next():
        actions.key("f4 alt-f")

    def find_previous():
        pass


@ctx.action_class("user")
class UserActions:
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

    def outlook_focus_message_list():
        actions.key("ctrl-1 alt f6:3")

    def outlook_focus_folder_list():
        actions.key("ctrl-1 alt f6:2")

    def outlook_focus_message_body():
        actions.key("ctrl-1 alt f6:4")

    def outlook_set_selected_folder(folder: str):
        actions.key("ctrl-y")
        actions.insert(actions.user.formatted_text(folder, "ALL_LOWERCASE"))
        actions.key("return")
