os: mac
-
^menu bar <user.text>$:
    key("cmd-shift-/")
    insert(user.text)

menu <user.text>:
    key(menu)
    insert(user.text)
