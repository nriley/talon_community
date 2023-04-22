app: safari
-
tag(): browser
tag(): user.tabs

# dictation mode gets confused when typing too fast
settings():
    insert_wait = 3
    key_wait = 3

tab group previous: key(cmd-shift-up)
tab group next: key(cmd-shift-down)

window reopen: key(cmd-shift-t)
window reopen all: user.menu_select("History|Reopen All Windows from Last Session")

reader: key(cmd-shift-r)
