#defines the commands that sleep/wake Talon
mode: all
-
^welcome back$:
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
^(talon|talent|talents|towns) sleep [<phrase>]$:
    speech.disable()
    user.enable_fd()
^(talon|talent|talents|towns) wake$:
    user.disable_fd()
    speech.enable()

key(ctrl-`):
    speech.toggle()
    user.disable_fd()
