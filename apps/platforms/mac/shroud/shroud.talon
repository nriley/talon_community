os: mac
-
focus app: user.shroud_focus_app()

focus window:
	user.shroud_ensure_running()
	key(ctrl-alt-w)
