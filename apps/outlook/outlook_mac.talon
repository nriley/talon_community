app.bundle: com.microsoft.Outlook
-
# dictation mode gets confused when typing too fast
settings():
    insert_wait = 2

archive: user.outlook_archive()
delete: key(cmd-backspace)
^delete all$: user.menu_select("Edit|Delete All")
flag: key(ctrl-5)
unflag: key(cmd-ctrl-')
junk: key(cmd-shift-j)
not junk: key(cmd-shift-alt-j)
download:
    user.outlook_download_images()
    user.outlook_focus_message_body()

mark [as] read: key(cmd-t)
mark [as] unread: key(cmd-shift-t)

# verb-noun vs noun-verb, retained for consistency with other
# knausj email apps
new message: key(cmd-n)
send [this] message: key(cmd-enter)

move: key(cmd-shift-m)

move to [<user.text>]:
    key(cmd-shift-m)
    insert(user.text or "")

reply: key(cmd-r)
reply all: key(cmd-shift-r)
forward: key(cmd-j)
defer | snooze | postpone: user.menu_select("Message|Snooze|Choose a Date")

hunt all: key(cmd-shift-f)

sync: key(cmd-ctrl-k)

toggle sidebar: key(cmd-alt-s)

# cmd-n is "page new", below
window (new | open): user.menu_select("File|New|Main Window")

# not tested in "old Outlook"
# can use Control-[/] for previous/next though that does not focus the message list
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

folder <user.text>:
    user.outlook_focus_folder_list()
    insert('{user.formatted_text(text, "ALL_LOWERCASE,NO_SPACES")}')
    user.outlook_focus_message_list()

go [to] inbox: user.outlook_set_selected_folder("inbox")
go [to] drafts: user.outlook_set_selected_folder("drafts")
go [to] junk: user.outlook_set_selected_folder("junk mail")
go [to] sent: user.outlook_set_selected_folder("sent items")

# new Outlook only (not exposed in scripting dictionary)
go [to] archive: user.outlook_set_selected_folder("archive")

# different implementation in "old Outlook" - replace above if you're using it
# flag: key(ctrl-5)
# unflag: user.outlook_unflag()

# message composition
bold: key(cmd-b)
italic: key(cmd-i)
underline: key(cmd-u)
strike through: key(cmd-shift-x)
normal: user.menu_select("Edit|Clear Formatting")

copy style: user.menu_select("Edit|Copy Formatting")
paste style: user.menu_select("Edit|Paste Formatting")

bullet: user.menu_select("Format|Bulleted List")

move right: key(cmd-])
move left: key(cmd-[)
