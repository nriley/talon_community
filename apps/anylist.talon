os: mac
and app.bundle: com.purplecover.anylist.mac
-

settings():
    insert_wait = 2

# https://help.anylist.com/articles/desktop-keyboard-shortcuts/

add [<user.text>]:
    key(esc a)
    text = text or ""
    "{user.formatted_text(text, 'CAPITALIZE_FIRST_WORD')}"

checked: key(esc h)
favorites: key(alt-f)
recent: key(alt-r)
filter: key(alt-l)

check: key(esc x)
edit:
    key(esc e)
    sleep(300ms)
    key(shift-tab)
favorite: key(esc f)
(save | done): key(cmd-enter)

# Quantity
less: key(-)
more: key(=)

previous | up: key(esc up)
next | down: key(esc down)

list next: key(cmd-down)
list previous: key(cmd-up)
lists toggle: key(ctrl-/)
