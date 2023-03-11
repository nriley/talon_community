from talon import Context, Module, actions, ui

ctx = Context()
mod = Module()
apps = mod.apps
mod.apps.safari = """
os: mac
and app.bundle: com.apple.Safari
"""

ctx.matches = r"""
app: safari
"""


@ctx.action_class("browser")
class BrowserActions:
    def address() -> str:
        window = ui.active_window()
        if not window:
            return ""
        try:
            toolbar = window.children.find_one(AXRole="AXToolbar", max_depth=0)
            address_field = toolbar.children.find_one(
                AXRole="AXTextField",
                AXIdentifier="WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD",
            )
            return address_field.AXValue
        except (ui.UIErr, AttributeError):
            pass
        try:
            return window.appscript().current_tab.URL(timeout=0.1)
        except:
            return ""

    def bookmark():
        actions.key("cmd-d")

    def bookmark_tabs():
        raise NotImplementedError(
            "Safari doesn't have a default shortcut for this functionality but it can be configured"
        )

    def bookmarks():
        actions.key("cmd-alt-b")

    def focus_address():
        actions.key("cmd-l")

    def focus_page():
        window = ui.active_window()
        if not window:
            return
        if not (sections := getattr(window.element, "AXSections")):
            return
        content = next(
            o["SectionObject"] for o in sections if o["SectionUniqueID"] == "AXContent"
        )
        content.AXFocused = True

    def focus_search():
        actions.browser.focus_address()

    def go(url: str):
        actions.browser.focus_address()
        actions.sleep("50ms")
        actions.insert(url)
        actions.key("enter")

    def go_blank():
        actions.key("cmd-n")

    def go_back():
        actions.key("cmd-[")

    def go_forward():
        actions.key("cmd-]")

    def go_home():
        actions.key("cmd-shift-h")

    def open_private_window():
        actions.key("cmd-shift-n")

    def reload():
        actions.key("cmd-r")

    def reload_hard():
        actions.key("cmd-alt-r")

    def show_clear_cache():
        raise NotImplementedError("Safari doesn't support this functionality")

    def show_downloads():
        actions.key("cmd-alt-l")

    def show_extensions():
        raise NotImplementedError()

    def show_history():
        actions.key("cmd-y")

    def submit_form():
        actions.key("enter")

    def toggle_dev_tools():
        actions.key("cmd-alt-i")


@ctx.action_class("user")
class UserActions:
    def browser_open_address_in_new_tab():
        actions.key("cmd-enter")

    def tab_jump(number: int):
        if number < 9:
            actions.key(f"cmd-{number}")

    def tab_final():
        actions.key("cmd-9")

    def tab_overview():
        actions.key("cmd-shift-\\")


@ctx.action_class("app")
class AppActions:
    def window_close():
        actions.key("cmd-shift-w")
