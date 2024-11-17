from talon import Context, Module, actions, app, ui

from .code_languages import code_languages, code_special_file_map

mod = Module()
ctx = Context()

ctx_forced = Context()
ctx_forced.matches = r"""
tag: user.code_language_forced
"""


mod.tag("code_language_forced", "This tag is active when a language mode is forced")
mod.list("language_mode", desc="Name of a programming language mode.")

# Maps spoken forms to language ids
ctx.lists["user.language_mode"] = {
    spoken_form: language.id
    for language in code_languages
    for spoken_form in language.spoken_forms
}

# Maps extension to language ids
extension_lang_map = {
    f".{ext}": lang.id for lang in code_languages for ext in lang.extensions
}

language_ids = {lang.id for lang in code_languages}
forced_language = ""
forced_language_by_wid = {}


@ctx.action_class("code")
class CodeActions:
    def language():
        file_name = actions.win.filename()
        if file_name in code_special_file_map:
            return code_special_file_map[file_name]

        file_extension = actions.win.file_ext().lower()
        return extension_lang_map.get(file_extension, "")


@ctx_forced.action_class("code")
class ForcedCodeActions:
    def language():
        return forced_language


def force_language(language):
    global forced_language
    forced_language = language
    # Update tags to force a context refresh. Otherwise `code.language` will not update.
    # Necessary to first set an empty list otherwise you can't move from one forced language to another.
    ctx.tags = []
    if language:
        ctx.tags = ["user.code_language_forced"]


@mod.action_class
class Actions:
    def code_set_language_mode(language: str):
        """Sets the active language mode, and disables extension matching"""
        global forced_language_by_wid
        assert language in language_extensions
        forced_language_by_wid[ui.active_window().id] = language
        force_language(language)
        actions.user.command_mode()

    def code_clear_language_mode():
        """Clears the active language mode, and re-enables code.language: extension matching"""
        global forced_language_by_wid
        forced_language_by_wid[ui.active_window().id] = ""
        force_language("")

    def code_show_forced_language_mode():
        """Show the active language for this context"""
        if forced_language:
            app.notify(f"Forced language: {forced_language}")
        else:
            app.notify("No language forced")


def on_focus(window):
    language = forced_language_by_wid.get(window.id)
    if language is not None:
        force_language(language)
    elif forced_language:
        forced_language_by_wid[window.id] = language


def on_close(win):
    if forced_language:
        forced_language_by_wid.pop(win.id, None)


def on_app(_):
    if forced_language:
        force_language("")


def on_ready():
    ui.register("win_focus", on_focus)
    ui.register("win_close", on_close)
    ui.register("app_activate", on_app)
    ui.register("app_deactivate", on_app)


app.register("ready", on_ready)
