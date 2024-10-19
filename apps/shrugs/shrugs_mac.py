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


@ctx.action_class("user")
class UserActions:
    # Navigation: Servers
    def messaging_workspace_previous():
        actions.key("cmd-{")

    def messaging_workspace_next():
        actions.key("cmd-}")

    # Navigation: Channels
    def messaging_channel_previous():
        # XXX DM support
        outline = channel_outline()
        selected_row_index = outline.AXSelectedRows[0].AXIndex
        if selected_row_index == 1:
            app.notify(
                title="Shrugs: No previous channel",
                body="This is already the first channel",
            )
            return
        prev_row = outline.children.find_one(
            AXRole="AXRow", AXIndex=selected_row_index - 1, max_depth=0
        )
        prev_row.AXSelected = True

    def messaging_channel_next():
        outline = channel_outline()
        selected_row_index = outline.AXSelectedRows[0].AXIndex
        try:
            next_row = outline.children.find_one(
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
        outline = channel_outline()
        selected_row_index = outline.AXSelectedRows[0].AXIndex
        for row in reversed(outline.AXRows):
            if row.AXIndex >= selected_row_index:
                continue
            if len(row.children[0].children) > 2:
                row.AXSelected = True
                return
        # XXX Go to previous unread server
        app.notify(title="Shrugs: No previous unread channel")

    def messaging_unread_next():
        outline = channel_outline()
        selected_row_index = outline.AXSelectedRows[0].AXIndex
        for row in outline.AXRows:
            if row.AXIndex <= selected_row_index:
                continue
            if len(row.children[0].children) > 2:
                row.AXSelected = True
                return
        # XXX Go to next unread server
        app.notify(title="Shrugs: No next unread channel")
