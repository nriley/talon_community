os: mac
app: mame
-

settings():
    key_wait = 5

app quit: key(cmd-alt-q)

capture: user.menu_select("Special|Capture Mouse")
