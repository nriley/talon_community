app: citrix_viewer_mac
-

# keys get dropped frequently, particularly during initial login
settings():
    insert_wait = 4

full screen: user.window_toggle_full_screen()

full screen all: user.citrix_use_all_displays_in_full_screen()

# Windows
start [<user.text>]:
    key(ctrl-esc)
    insert(text or "")

control (alt | alter) delete: key(ctrl-cmd-del)
