app: citrix_viewer_mac
-

# bridged clipboard isn't that fast or reliable
tag(): user.no_paste_to_insert

settings():
    # keys get dropped frequently, particularly during initial login
    insert_wait = 4
    key_wait = 6

full screen: user.window_toggle_full_screen()

# Windows
start [<user.text>]:
    key(ctrl-esc)
    insert(text or "")

control (alt | alter) delete: user.menu_select("Devices|Keyboard|Send Ctrl-Alt-Del")
