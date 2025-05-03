from talon import Context, Module, actions, app, ui

mod = Module()
ctx = Context()

mod.apps.keynote = r"""
os: mac
and app.bundle: com.apple.iWork.Keynote
"""

ctx.matches = r"""
os: mac
app: keynote
"""

ctx_presentation = Context()
ctx_presentation.matches = r"""
app: keynote
mode: user.presentation
"""


@ctx.action_class("user")
class UserActions:
    # user.pages
    def page_next():
        doc = keynote_doc()
        current_slide_number = doc.current_slide.slide_number()
        last_slide_number = doc.slides.last.slide_number()
        if current_slide_number < last_slide_number:
            doc.current_slide.set(doc.slides[current_slide_number + 1])

    def page_previous():
        doc = keynote_doc()
        current_slide_number = doc.current_slide.slide_number()
        if current_slide_number > 1:
            doc.current_slide.set(doc.slides[current_slide_number - 1])

    def page_final():
        doc = keynote_doc()
        doc.current_slide.set(doc.slides.last)


@ctx_presentation.action_class("user")
class UserActions:
    # user.pages
    def page_next():
        keynote_app().appscript().show_next()

    def page_previous():
        keynote_app().appscript().show_previous()


KEYNOTE_BUNDLE_ID = "com.apple.iWork.Keynote"


def keynote_app():
    return ui.apps(bundle=KEYNOTE_BUNDLE_ID)[0]


def keynote_doc():
    return keynote_app().appscript().documents[1]


def is_keynote(app):
    return app.bundle == KEYNOTE_BUNDLE_ID


def win_opened(window):
    if not is_keynote(window.app) or not window.doc:
        return
    if window.element.get("AXTitleUIElement"):
        actions.user.exit_user_mode("presentation")
    else:
        actions.user.enter_user_mode("presentation")


def ready():
    ui.register("win_open", win_opened)


app.register("ready", ready)
