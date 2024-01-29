from talon import Context, Module, actions, app, ui

if app.platform == "mac":
    from appscript import k, its

ctx = Context()
mod = Module()

ctx.matches = r"""
app: word_mac
"""


def word_app():
    return ui.apps(bundle="com.microsoft.Word")[0]


def word_document_window():
    if not (active_window := ui.active_window()):
        raise Exception("Can't determine active window")

    word = word_app()

    if active_window.app != word:
        raise Exception("Word is not frontmost")

    if not active_window.doc:  # remote documents don't return anything
        e = active_window.element
        if (
            e.AXSubrole != "AXStandardWindow"
            or e.get("AXFullScreenButton") is None
            or e.get("AXDefaultButton") is not None
        ):
            raise Exception("Frontmost window is not a document window")

    return word.appscript().windows[its.active == True]()[0]


def word_document_zoom():
    return word_document_window().view.zoom


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.user.menu_select("Window|New Window")


@ctx.action_class("edit")
class EditActions:
    def zoom_in():
        zoom = word_document_zoom()
        zoom.percentage.set(zoom.percentage() * 1.25)

    def zoom_out():
        zoom = word_document_zoom()
        zoom.percentage.set(zoom.percentage() / 1.25)

    def zoom_reset():
        word_document_zoom().percentage.set(100)


@ctx.action_class("user")
class UserActions:
    def find(text: str):
        actions.key("cmd-f")
        if text:
            actions.insert(text)

    def find_next():
        actions.key("cmd-g")

    def find_previous():
        actions.key("cmd-shift-g")

    def find_everywhere(text: str):
        actions.user.menu_select("Edit|Find|Advanced Find and Replace...")
        if text:
            actions.insert(text)

    def find_toggle_match_by_case():
        pass  # could implement

    def find_toggle_match_by_word():
        pass

    def find_toggle_match_by_regex():
        pass

    def replace(text: str):
        actions.user.menu_select("Edit|Find|Replace...")
        if text:
            actions.insert(text)

    replace_everywhere = replace

    def replace_confirm():
        pass

    def replace_confirm_all():
        pass

    def select_previous_occurrence(text: str):
        actions.edit.find(text)
        actions.edit.find_previous()
        actions.key("esc")

    def select_next_occurrence(text: str):
        actions.edit.find(text)
        actions.edit.find_next()
        actions.key("esc")

    def zoom_to_fit():
        word_document_zoom().page_fit.set(k.page_fit_full_page)

    def zoom_to_fit_width():
        word_document_zoom().page_fit.set(k.page_fit_best_fit)
