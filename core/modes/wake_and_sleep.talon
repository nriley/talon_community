#defines the commands that sleep/wake Talon
mode: all
-
^(welcome back)+$:
    user.mouse_wake()
    user.history_enable()
    user.talon_mode()
^sleep all [<phrase>]$:
    user.switcher_hide_running()
    user.history_disable()
    user.homophones_hide()
    user.help_hide()
    user.mouse_sleep()
    speech.disable()
    user.engine_sleep()
^snore [<phrase>]$: speech.disable()
^(talon wake)+$:
    user.disable_fd()
    speech.enable()

key(ctrl-`):
    speech.toggle()
    user.disable_fd()
