os: windows
and app.exe: OUTLOOK.EXE
-
tag(): user.find_and_replace

archive:
    user.outlook_focus_message_list()
    key(backspace)
flag: key(alt-h u a)
unflag: key(alt-h u e)
junk: key(alt-h j b)

new message: key(ctrl-n)
send [this] message: key(alt-s)

move: key(ctrl-shift-v)

move to [<user.text>]:
    key(ctrl-shift-v)
    insert(user.text or "")

reply: key(ctrl-r)
reply all: key(ctrl-shift-r)

next:
    user.outlook_focus_message_list()
    key(down)
previous:
    user.outlook_focus_message_list()
    key(up)
collapse:
    user.outlook_focus_message_list()
    key(left)
expand:
    user.outlook_focus_message_list()
    key(right)
message: user.outlook_focus_message_body()
