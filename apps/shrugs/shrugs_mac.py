from talon import Context, Module, actions, app, ui

mod = Module()
ctx = Context()

mod.apps.shrugs = r"""
os: mac
and app.bundle: de.zeezide.swift.see1.shrugs
"""

ctx.matches = r"""
os: mac
app: shrugs
"""


def shrugs():
    return ui.apps(bundle="de.zeezide.swift.see1.shrugs")[0]


def channel_outline():
    return (
        shrugs()
        .active_window.element.children.find_one(AXRole="AXSplitGroup", max_depth=0)
        .children.find_one(AXIdentifier="sidebar-content", max_depth=0)
        .children.find_one(AXRole="AXOutline", max_depth=0)
    )


def workspace_table():
    return (
        shrugs()
        .active_window.element.children.find_one(AXRole="AXSplitGroup", max_depth=0)
        .children.find_one(AXIdentifier="SlickServicesIconPaneVC", max_depth=0)
        .children.find_one(AXRole="AXTable", max_depth=0)
    )


@mod.action_class
class Actions:
    def shrugs_channel_reload():
        """Go to the next and then previous channel in order to work around
        a Shrugs bug in which the channel contents do not appear"""


def go_unread(go_next=True):
    workspaces = None
    selected_row_index = None

    while True:
        channels = channel_outline()
        channel_rows = channels.AXRows
        if selected_row_index is None:
            selected_row_index = channels.AXSelectedRows[0].AXIndex
        elif go_next:
            selected_row_index = 0
        else:
            selected_row_index = len(channel_rows) + 2
        if not go_next:
            channel_rows = reversed(channel_rows)
        for row in channel_rows:
            if go_next:
                if row.AXIndex <= selected_row_index:
                    continue
            elif row.AXIndex >= selected_row_index:
                continue
            if len(row.children[0].children) > 2:
                row.AXSelected = True
                return True
        # Server unread indicator/count is not exposed via accessibility
        if workspaces is None:
            workspaces = workspace_table()
            workspace_rows = workspaces.AXRows
            original_workspace_index = workspaces.AXSelectedRows[0].AXIndex
            selected_row_index = original_workspace_index
        else:
            selected_row_index = workspaces.AXSelectedRows[0].AXIndex
        if go_next:
            selected_row_index += 1
            if selected_row_index >= len(workspace_rows):
                selected_row_index = original_workspace_index
        else:
            selected_row_index -= 1
            if selected_row_index < 0:
                selected_row_index = original_workspace_index
        workspace_rows[selected_row_index].AXSelected = True
        if selected_row_index == original_workspace_index:
            return False


@ctx.action_class("user")
class UserActions:
    def shrugs_channel_reload():
        outline = channel_outline()
        selected_row_index = outline.AXSelectedRows[0].AXIndex
        if selected_row_index == 1:
            actions.user.messaging_channel_next()
            actions.user.messaging_channel_previous()
        else:
            actions.user.messaging_channel_previous()
            actions.user.messaging_channel_next()

    # Navigation: Servers
    def messaging_workspace_previous():
        actions.key("cmd-{")

    def messaging_workspace_next():
        actions.key("cmd-}")

    # Navigation: Channels
    def messaging_channel_previous():
        # XXX DM support
        channels = channel_outline()
        selected_row_index = channels.AXSelectedRows[0].AXIndex
        if selected_row_index == 1:
            app.notify(
                title="Shrugs: No previous channel",
                body="This is already the first channel",
            )
            return
        prev_row = channels.children.find_one(
            AXRole="AXRow", AXIndex=selected_row_index - 1, max_depth=0
        )
        prev_row.AXSelected = True

    def messaging_channel_next():
        channels = channel_outline()
        selected_row_index = channels.AXSelectedRows[0].AXIndex
        try:
            next_row = channels.children.find_one(
                AXRole="AXRow", AXIndex=selected_row_index + 1, max_depth=0
            )
        except ui.UIErr:
            app.notify(
                title="Shrugs: No next channel",
                body="Is this the last channel?",
            )
            return
        next_row.AXSelected = True

    def messaging_unread_previous():
        if not go_unread(go_next=False):
            app.notify(title="Shrugs: No previous unread channel")

    def messaging_unread_next():
        if not go_unread():
            app.notify(title="Shrugs: No next unread channel")

    def messaging_mark_channel_read():
        actions.user.menu_select("Conversation|Mark All as Unread")
