os: mac
-
# Vimac/Homerow "classic" (labels)
^nav$: key(ctrl-alt-v)

# Homerow Redux (UI search)
^row [<user.text>]:
    key(ctrl-alt-shift-h)
    sleep(50ms)
    insert(text or "")
