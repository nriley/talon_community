app: safari
-
# dictation mode gets confused when typing too fast
settings():
	key_wait = 3

window reopen: key(cmd-shift-t)
window reopen all: user.menu_select('History|Reopen All Windows from Last Session')
