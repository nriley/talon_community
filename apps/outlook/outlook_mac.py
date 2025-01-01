from talon import Context, Module, actions, app, ctrl, ui
from talon.mac import applescript

ctx = Context()
mod = Module()

ctx.matches = r"""
app: outlook_mac
"""


def outlook_app():
    return ui.apps(bundle="com.microsoft.Outlook")[0]


def outlook_focused_element():
    outlook = outlook_app()
    seen_nothing = False
    for attempt in range(10):
        element = outlook.focused_element
        if element and getattr(element, "AXRole", None):
            return element
        # XXX relative of https://github.com/talonvoice/talon/issues/480
        element = ui.focused_element()
        if element and getattr(element, "AXRole", None):
            return element
        if not seen_nothing:
            # attempt to work around Outlook issue where nothing appears focused
            # (via either method; outlook.element.AXFocusedUIElement is None)
            actions.key("ctrl-shift-[ ctrl-shift-]")
            seen_nothing = True
        actions.sleep("50ms")
    else:
        raise Exception("Unable to determine focused element in Outlook")


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.user.menu_select("File|New|Main Window")


def zoom_if_editing(out: bool):
    zoom_item = (
        outlook_app()
        .element.children.find_one(AXRole="AXMenuBar", max_depth=0)
        .children.find_one(AXRole="AXMenuBarItem", AXTitle="Format", max_depth=0)
        .children[0]
        .children.find_one(AXRole="AXMenuItem", AXTitle="Zoom", max_depth=0)
    )
    if not zoom_item.AXEnabled:
        return False

    element_center = outlook_focused_element().AXFrame.center
    actions.key("ctrl:down")
    # y scroll amount maps directly to zoom percentage; keyboard zooming in a message
    # zooms by 20% at a time, so do the same here. But, depending on the current
    # zoom level, this may do nothing - an Outlook bug I'm not working around
    ctrl.mouse_scroll(y=(-20 if out else 20), pos=tuple(element_center))
    actions.key("ctrl:up")

    return True


@ctx.action_class("edit")
class EditActions:
    def zoom_in():
        if zoom_if_editing(False):
            return
        actions.key("cmd-=")

    def zoom_out():
        if zoom_if_editing(True):
            return
        actions.key("cmd--")


@ctx.action_class("user")
class UserActions:
    def find_everywhere(text: str):
        actions.key("cmd-shift-f")
        if text:
            actions.insert(text)

    def outlook_set_selected_folder(folder: str):
        # for "old Outlook" this uses the scripting dictionary
        # for "new Outlook" this currently uses the displayed folder name
        result = applescript.run(
            f"""
			tell application id "com.microsoft.Outlook"
				if (exists (selected folder)) then
					set selected folder to {folder}
					return true
				end if
				return false
			end tell"""
        )
        if result == "false":
            # new Outlook (at least until it gets OSA support)
            actions.user.outlook_focus_folder_list()
            actions.insert(folder)
            actions.user.outlook_focus_message_list()

    def outlook_archive():
        actions.user.outlook_focus_message_list()
        actions.key("ctrl-e")

    def outlook_unflag():
        applescript.run(
            """
			tell application id "com.microsoft.Outlook"
				get selected objects
				repeat with _object in result
					if _object's class is (incoming message) and _object's todo flag is not (not flagged) then
						set todo flag of _object to not flagged
					end if
				end repeat
			end tell"""
        )

    def outlook_focus_message_list():
        outlook = outlook_app()

        element = outlook_focused_element()
        if (
            element.AXRole == "AXGroup"
            and element.get("AXIdentifier") == "Email Renderer View"
        ):
            # Outlook is in a state in which keyboard controls message list but focus
            # is in the message body (likely intended, but confusing when inspecting).
            # This is the case immediately after selecting a folder, for example.
            # XXX ...unfortunately, sometimes this is NOT the case and I don't know
            # XXX how to tell the difference from accessibility
            return

        last_focused_element = None
        for attempt in range(10):
            focused_element = outlook_focused_element()
            role = focused_element.AXRole
            if focused_element != last_focused_element:
                if role == "AXTable":
                    return
                actions.key("ctrl-shift-]")
            last_focused_element = focused_element
            actions.sleep("50ms")

        raise Exception(
            f"Unable to focus Outlook message list, instead focused {focused_element}"
        )

    def outlook_focus_folder_list():
        outlook = outlook_app()
        toolbar_split = outlook.active_window.children.find_one(
            AXRole="AXSplitGroup", max_depth=0
        )
        sidebar_split = toolbar_split.children.find_one(
            AXRole="AXSplitGroup", max_depth=0
        )
        scroll_area_or_split_group = sidebar_split.children[0]
        if scroll_area_or_split_group.AXRole != "AXScrollArea":
            actions.key("cmd-alt-s")

        last_focused_element = None
        for attempt in range(10):
            focused_element = outlook_focused_element()
            role = focused_element.AXRole
            if focused_element != last_focused_element:
                if role == "AXOutline":
                    return
                actions.key("ctrl-shift-[")
            last_focused_element = focused_element
            actions.sleep("50ms")

        app.notify(
            "Unable to focus Outlook folder list",
            body="If this keeps happening, consider closing and reopening the Outlook window",
        )
        raise Exception("Unable to focus Outlook folder list")

    def outlook_download_images():
        outlook = outlook_app()
        toolbar_split = outlook.active_window.children.find_one(
            AXRole="AXSplitGroup", max_depth=0
        )
        sidebar_split = toolbar_split.children.find_one(
            AXRole="AXSplitGroup", max_depth=0
        )
        list_split = sidebar_split.children.find_one(AXRole="AXSplitGroup", max_depth=0)
        infobar = list_split.children.find_one(
            AXRole="AXScrollArea", AXTitle="Infobar View", max_depth=0
        )
        download_button = infobar.children.find_one(AXRole="AXButton", max_depth=0)
        download_button.perform("AXPress")

    def outlook_focus_message_body():
        outlook = outlook_app()

        last_focused_element = None
        for attempt in range(10):
            focused_element = outlook_focused_element()
            role = focused_element.AXRole
            if focused_element != last_focused_element:
                if (
                    role == "AXGroup"
                    and focused_element.get("AXIdentifier", None)
                    != "Email Renderer View"
                ) or (role in ("AXTextArea", "AXWebArea")):
                    return
                actions.key("ctrl-shift-[")
            last_focused_element = focused_element
            actions.sleep("50ms")

        raise Exception("Unable to focus Outlook message body")


@mod.action_class
class Actions:
    def outlook_set_selected_folder(folder: str):
        """Open the specified folder in Outlook"""

    def outlook_archive():
        """Archive the selected messages in Outlook"""

    def outlook_unflag():
        """Remove flag from selected messages in Outlook"""

    def outlook_focus_message_body():
        """Focus the message body in Outlook"""

    def outlook_focus_message_list():
        """Focus the message list in Outlook"""

    def outlook_focus_folder_list():
        """Focus the folder list in Outlook"""

    def outlook_download_images():
        """Download images in Outlook"""
