from talon import ctrl, ui, Module, Context, actions, clip, app

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
ctx.tags = ['browser', 'user.tabs']

@ctx.action_class('browser')
class BrowserActions:
    def address() -> str: 
        window = ui.active_window()
        if not window:
            return ''
        try:
            toolbar = window.children.find_one(AXRole='AXToolbar', max_depth=0)
            address_field = toolbar.children.find_one(
                AXRole='AXTextField', AXIdentifier='WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD')
            return address_field.AXValue
        except (ui.UIErr, AttributeError):
            pass
        try:
            return window.appscript().current_tab.URL(timeout=0.1)
        except:
            return ''
    def bookmark():
        actions.key('cmd-d')
    def bookmark_tabs():
        actions.key('cmd-shift-d')
    def bookmarks():
        actions.key('cmd-alt-b')
    #action(browser.bookmarks_bar):
    #	key(ctrl-shift-b)
    def focus_address():
        actions.key('cmd-l')
        #action(browser.focus_page):
    def focus_page():
        actions.key('escape:2')
    def focus_search():
        actions.browser.focus_address()
    def go(url: str):
        actions.browser.focus_address()
        actions.sleep("50ms")
        actions.insert(url)
        actions.key("enter")
    def go_blank():
        actions.key('cmd-n')
    def go_back():
        actions.key('cmd-[')
    def go_forward():
        actions.key('cmd-]')
    def go_home():
        actions.key('cmd-shift-h')
    def open_private_window():
        actions.key('cmd-shift-n')
    def reload():
        actions.key('cmd-r')
    def reload_hard():
        actions.key('cmd-shift-r')
    #action(browser.reload_hardest):
    #action(browser.show_clear_cache):
    #	key(cmd-shift-delete)
    def show_downloads():
        actions.key('cmd-alt-l')
    # def show_extensions():
    #     actions.key('ctrl-shift-a')
    def show_history():
        actions.key('cmd-y')
    def submit_form():
        actions.key('enter')
    #action(browser.title)
    def toggle_dev_tools():
        actions.key('cmd-alt-i')

@ctx.action_class('user')
class UserActions:
    def tab_jump(number: int):
        if number < 9:
            actions.key("cmd-{}".format(number))

    def tab_final():
        actions.key("cmd-9")

    def tab_overview():
        actions.key('cmd-shift-\\')
