^force {user.language_mode}$:
    user.code_set_language_mode(language_mode)
    app.notify("Forced language mode {language_mode}")
^clear language modes$:
    user.code_clear_language_mode()
    app.notify("Cleared language modes")
