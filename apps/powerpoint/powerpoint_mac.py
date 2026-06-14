import re

from talon import Context, Module, actions, app, ui

ctx = Context()
mod = Module()

ctx.matches = r"""
app: powerpoint_mac
"""

ctx_presentation = Context()
ctx_presentation.matches = r"""
app: powerpoint_mac
mode: user.presentation
"""

RE_SLIDE_SHOW = re.compile(r"PowerPoint Slide Show - \[.*\]")
RE_PRESENTING = re.compile(r"PowerPoint (Slide Show|Presenter View) - \[.*\]")


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.user.menu_select("Window|New Window")


@ctx.action_class("user")
class UserActions:
    def copy_style():
        actions.key("cmd-shift-c")

    def paste_style():
        actions.key("cmd-shift-v")

    def zoom_to_fit():
        actions.key("cmd-alt-o")

    # user.pages
    def page_next():
        actions.key("pagedown")

    def page_previous():
        actions.key("pageup")

    def page_final():
        actions.key("end")


@ctx_presentation.action_class("user")
class PresentationUserActions:
    # user.pages
    def page_next():
        actions.key("pagedown")

    def page_previous():
        actions.key("pageup")


POWERPOINT_BUNDLE_ID = "com.microsoft.Powerpoint"


def is_powerpoint(app):
    return app.bundle == POWERPOINT_BUNDLE_ID


def win_opened(window):
    if is_powerpoint(window.app) and RE_SLIDE_SHOW.match(window.title):
        actions.user.enter_user_mode("presentation")


def win_focused(window):
    if is_powerpoint(window.app) and not RE_PRESENTING.match(window.title):
        actions.user.exit_user_mode("presentation")


def ready():
    ui.register("win_open", win_opened)
    ui.register("win_focus", win_focused)


app.register("ready", ready)
