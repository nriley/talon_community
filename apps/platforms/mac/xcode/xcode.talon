os: mac
and app.bundle: com.apple.dt.Xcode
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.tabs

file:
    key(cmd-shift-o)

file name <user.text>:
    key(cmd-shift-o)
    insert(user.text)
