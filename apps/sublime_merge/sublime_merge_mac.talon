app.bundle: com.sublimemerge
-
tag(): user.tabs
tag(): user.file_manager

please [<user.text>]:
    key(cmd-shift-p)
    insert(user.text or "")

^message [<user.prose>]$:
    key(cmd-9)
    sleep(100ms)
    user.insert_formatted(prose or "", "CAPITALIZE_FIRST_WORD")

^message previous:
    key(cmd-9)
    sleep(100ms)
    key(cmd-; down)

go locations: key(cmd-1)
go commits: key(cmd-2)
go files: key(cmd-3)

commit:
    key(cmd-9)
    sleep(100ms)
    key(cmd-enter)
push: key(cmd-alt-up)
pull: key(cmd-alt-down)
# XXX broken - see https://github.com/sublimehq/sublime_merge/issues/778
# stage: key(shift-enter)
stage all:
    key(cmd-shift-a)
    sleep(100ms)
stage untracked: key(cmd-k cmd-a)

stash: key(cmd-s)
stash pop: key(cmd-shift-s)

branch: key(cmd-b)
branch new: key(cmd-shift-b)

^repo next: key(ctrl-tab)
^repo previous: key(shift-ctrl-tab)

^repo [<user.text>]:
    key(escape ctrl-cmd-p)
    insert('{user.formatted_text(text or "", "ALL_LOWERCASE,NO_SPACES")}')
