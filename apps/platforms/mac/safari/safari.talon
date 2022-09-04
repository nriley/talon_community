app: safari
-
# dictation mode gets confused when typing too fast
settings():
	key_wait = 3

tab group previous: key(cmd-shift-up)
tab group next: key(cmd-shift-down)

window reopen: key(cmd-shift-t)
window reopen all: user.menu_select('History|Reopen All Windows from Last Session')
