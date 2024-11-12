from talon import Context, Module, actions, app, ui

# Maps language mode names to the extensions that activate them. Only put things
# here which have a supported language mode; that's why there are so many
# commented out entries. TODO: make this a csv file?
language_extensions = {
    # 'assembly': 'asm s',
    # 'bash': 'bashbook sh',
    "batch": "bat",
    "c": "c h",
    # 'cmake': 'cmake',
    # "cplusplus": "cpp hpp",
    "csharp": "cs",
    "css": "css",
    # 'elisp': 'el',
    # 'elm': 'elm',
    "gdb": "gdb",
    "go": "go",
    "java": "java",
    "javascript": "js",
    "javascriptreact": "jsx",
    # "json": "json",
    "elixir": "ex",
    "kotlin": "kt",
    "lua": "lua",
    "m": "rou",
    "markdown": "md",
    # 'perl': 'pl',
    "php": "php",
    # 'powershell': 'ps1',
    "python": "py",
    "protobuf": "proto",
    "r": "r",
    # 'racket': 'rkt',
    "ruby": "rb",
    "rust": "rs",
    "scala": "scala",
    "scss": "scss",
    # 'snippets': 'snippets',
    "sql": "sql",
    "stata": "do ado",
    "talon": "talon",
    "talonlist": "talon-list",
    "terraform": "tf",
    "tex": "tex",
    "typescript": "ts",
    "typescriptreact": "tsx",
    # 'vba': 'vba',
    "vimscript": "vim vimrc",
    # html doesn't actually have a language mode, but we do have snippets.
    "html": "html",
}

# Files without specific extensions but are associated with languages
special_file_map = {
    "CMakeLists.txt": "cmake",
    "Makefile": "make",
    "Dockerfile": "docker",
    "meson.build": "meson",
    ".bashrc": "bash",
    ".zshrc": "zsh",
    "PKGBUILD": "pkgbuild",
    ".vimrc": "vimscript",
    "vimrc": "vimscript",
}

# Override speakable forms for language modes. If not present, a language mode's
# name is used directly.
language_name_overrides = {
    "cplusplus": ["see plus plus"],
    "csharp": ["see sharp"],
    "css": ["c s s"],
    "gdb": ["g d b"],
    "go": ["go", "go lang", "go language"],
    "r": ["are language"],
    "sql": ["s q l", "sequel"],
    "tex": ["tech", "lay tech", "latex"],
}

mod = Module()
ctx = Context()

ctx_forced = Context()
ctx_forced.matches = r"""
tag: user.code_language_forced
"""


mod.tag("code_language_forced", "This tag is active when a language mode is forced")
mod.list("language_mode", desc="Name of a programming language mode.")

ctx.lists["self.language_mode"] = {
    name: language
    for language in language_extensions
    for name in language_name_overrides.get(language, [language])
}

# Maps extension to languages.
extension_lang_map = {
    "." + ext: language
    for language, extensions in language_extensions.items()
    for ext in extensions.split()
}

language_ids = set(language_extensions.keys())

forced_language = ""
forced_language_by_wid = {}


@ctx.action_class("code")
class CodeActions:
    def language():
        file_name = actions.win.filename()
        if file_name in special_file_map:
            return special_file_map[file_name]

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
