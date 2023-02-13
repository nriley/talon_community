app.bundle: com.apple.mail
-
archive: key(ctrl-cmd-a)
delete: key(backspace)
# This toggles; OK for now
flag | unflag: key(cmd-shift-l)
junk: key(cmd-shift-j)
reply: key(cmd-r)
reply all: key(cmd-shift-r)

send [this] message: key(cmd-shift-d)

# uses my favorite mailboxes
go [to] inbox: key(cmd-1)
go [to] drafts: key(cmd-4)
go [to] sent: key(cmd-2)

next: user.mail_select_message(1)
previous: user.mail_select_message(-1)

message (last | lost | lust):
    key(end)
    user.mail_select_last_message()

normal: user.menu_select("Format|Style|Remove Style")

# MsgFiler
move: key(ctrl-s)

(save to | move to | folder) [<user.text>]:
    key(ctrl-s)
    sleep(200ms)
    insert(user.text or "")

# Add to OmniFocus
to do: key(ctrl-o)
