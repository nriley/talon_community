os: mac
and app.bundle: com.purplecover.anylist.mac
-

# https://help.anylist.com/articles/desktop-keyboard-shortcuts/

add [<user.text>]:
    key(esc a)
    text = text or ""
    "{user.formatted_text(text, 'CAPITALIZE_FIRST_WORD')}"

checked: key(h)

check | done: key(x)
edit:
    key(e)
    sleep(300ms)
    key(shift-tab)
favorite: key(f)
save: key(cmd-enter)

less: key(-)
more: key(=)

previous | up: key(up)
next | down: key(down)
