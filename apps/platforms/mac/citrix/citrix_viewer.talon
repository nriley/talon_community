app: citrix_viewer
-

# keys get dropped frequently, particularly during initial login
settings():
	insert_wait = 2

full screen: user.window_toggle_full_screen()

full screen all: user.citrix_use_all_displays_in_full_screen()

# Windows
start [<user.text>]:
	key(ctrl-esc)
	insert(text or "")
