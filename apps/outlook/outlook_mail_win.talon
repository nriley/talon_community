app: outlook_mail_win
-
tag(): user.find_and_replace

archive: key(alt-h o 1)
flag: key(alt-h u a)
unflag: key(alt-h u e esc:3)
junk: key(alt-h j b)
not junk: key(ctrl-alt-j)
download: key(ctrl-shift-w p)

mark [as] read: key(ctrl-q)
mark [as] unread: key(ctrl-u)

new message: key(ctrl-n)
send [this] message: key(alt-s)

move: key(ctrl-shift-v)

move to [<user.text>]:
    key(ctrl-shift-v)
    insert(user.text or "")

reply: key(ctrl-r)
reply all: key(ctrl-shift-r)
forward: key(ctrl-f)
defer | snooze | postpone: key(alt-h u c alt-r tab:2 space)

next: key(ctrl-.)
previous: key(ctrl-,)
collapse:
    user.outlook_focus_message_list()
    key(left)
expand:
    user.outlook_focus_message_list()
    key(right)
message: user.outlook_focus_message_body()

folder <user.text>:
    key(ctrl-y)
    insert('{user.formatted_text(text, "ALL_LOWERCASE")}')

go [to] inbox: key(ctrl-shift-i)
go [to] drafts: user.outlook_set_selected_folder("drafts")
go [to] junk: user.outlook_set_selected_folder("junk email")
go [to] sent: user.outlook_set_selected_folder("sent items")
go [to] archive: user.outlook_set_selected_folder("archive")
