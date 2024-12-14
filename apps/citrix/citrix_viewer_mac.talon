app: citrix_viewer_mac
-

settings():
    # keys get dropped frequently, particularly during initial login
    insert_wait = 4
    # bridged clipboard isn't that fast or reliable
    user.paste_to_insert_threshold = -1

full screen: user.window_toggle_full_screen()

full screen all: user.citrix_use_all_displays_in_full_screen()

# Windows
start [<user.text>]:
    key(ctrl-esc)
    insert(text or "")

control (alt | alter) delete: key(ctrl-cmd-del)
