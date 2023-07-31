os: windows
and app.exe: sublime_merge.exe
-
tag(): user.tabs

please [<user.text>]:
    key(ctrl-shift-p)
    insert(user.text or "")

^message [<user.prose>]$:
    key(ctrl-9)
    sleep(100ms)
    user.insert_formatted(prose or "", "CAPITALIZE_FIRST_WORD")

^message previous:
    key(ctrl-9)
    sleep(100ms)
    key(ctrl-; down)

go locations: key(ctrl-1)
go commits: key(ctrl-2)
go files: key(ctrl-3)

commit: key(ctrl-9 ctrl-enter)
push: key(ctrl-alt-up)
pull: key(ctrl-alt-down)
stage all:
    key(ctrl-shift-a)
    sleep(100ms)
stage untracked: key(ctrl-k ctrl-a)

stash: key(ctrl-s)
stash pop: key(ctrl-shift-s)

branch: key(ctrl-b)
branch new: key(ctrl-shift-b)

^branch [<user.text>]:
    key(escape ctrl-b)
    insert('{user.formatted_text(text or "", "ALL_LOWERCASE,NO_SPACES")}')

^repo next: key(ctrl-tab)
^repo previous: key(shift-ctrl-tab)

^repo [<user.text>]:
    key(ctrl-shift-o)
    insert('{user.formatted_text(text or "", "ALL_LOWERCASE,NO_SPACES")}')

# Win+down x2 does not reliably minimize the window
window minimize: key(alt-space n)
