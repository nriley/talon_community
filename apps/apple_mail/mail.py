from talon import Context, Module, actions, ui

mod = Module()
ctx = Context()

ctx.matches = """
os: mac
and app.bundle: com.apple.mail
"""


def mail_app():
    return ui.apps(bundle="com.apple.mail")[0]


def mail_messages_table():
    mail = mail_app()
    try:
        return mail.active_window.children.find_one(
            AXRole="AXTable", AXDescription="messages", max_depth=3
        )
    except ui.UIErr:
        return None  # no messages table found


def mail_front_message_viewer():
    mail = mail_app().appscript()
    front_window = mail.windows[1]()
    for i, message_viewer_window in enumerate(mail.message_viewers.window()):
        if message_viewer_window == front_window:
            return mail.message_viewers[i]
    else:
        app.notify("Unable to locate front message viewer")
        return None


def mail_selected_messages():
    if (message_viewer := mail_front_message_viewer()) is not None:
        return message_viewer.selected_messages()

    return None


@ctx.action_class("user")
class UserActions:
    def mail_select_last_message():
        if not (messages_table := mail_messages_table()):
            return

        last_row = [
            child for child in messages_table.children if child.AXRole == "AXRow"
        ][-1]
        last_row.AXSelected = True

    def mail_select_message(offset: int):
        if not (messages_table := mail_messages_table()):
            return

        try:  # filtering this way is ~2x as fast as using AXSelectedRows
            selected_row = messages_table.children.find_one(
                AXSelected=True, max_depth=0
            )
        except ui.UIErr:
            return

        # index (in all children, not just rows) of first selected row
        desired_index = selected_row.AXIndex + offset
        desired_index = max(desired_index, 0)

        children = list(messages_table.children)
        desired_index = min(desired_index, len(children) - 1)

        # don't get stuck in column headers
        while children[desired_index].AXRole != "AXRow":
            desired_index += 1
            if desired_index >= len(children):
                return

        children[desired_index].AXSelected = True

    def find_everywhere(text: str):
        actions.key("cmd-alt-f")
        actions.insert(text)

    def mail_mark_as_read():
        for selected_message in mail_selected_messages():
            selected_message.read_status.set(True)

    def mail_mark_as_unread():
        for selected_message in mail_selected_messages():
            selected_message.read_status.set(False)

    def mail_download_images():
        mail = mail_app()
        try:
            mail.active_window.element.children.find_one(
                AXRole="AXGroup", AXDescription="load failed proxy content banner"
            ).children.find_one(AXRole="AXButton").perform("AXPress")
        except ui.UIErr:
            pass


@mod.action_class
class Actions:
    def mail_select_last_message():
        """Select the last message in the currently focused Apple Mail message viewer"""

    def mail_select_message(offset: int):
        """Navigate to message offset from selected message"""

    def mail_mark_as_read():
        """Mark the selected messages as read"""

    def mail_mark_as_unread():
        """Mark the selected messages as unread"""

    def mail_download_images():
        """Download images in Apple Mail"""
