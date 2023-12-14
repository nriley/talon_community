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

# navigate to first hunk in file (or section in Summary tab)
hunk:
    key(cmd-shift-[ cmd-shift-])
    sleep(150ms)
    key(tab)

commit:
    key(cmd-9)
    sleep(100ms)
    key(cmd-enter)
push: key(cmd-alt-up)
push force:
    key(shift-f8)
    "--force-with-lease"
    key(enter)
pull: key(cmd-alt-down)

# stage commands work when insertion point is in a hunk

# this tends to get preferred to other stage commands (and can be destructive to your carefully curated
# commit); feel free to uncomment if you don't see the conflict
# ^stage | unstage$: key(shift-enter)

(stage | unstage) (this | hunk | lines): key(enter)

# stage command works in a file tab
stage file: key(cmd-shift-[ cmd-shift-] tab shift-enter)

# stage commands work anywhere in a commit
stage all:
    key(cmd-shift-a)
    sleep(100ms)
unstage all: key(cmd-shift-r)
stage untracked: key(cmd-k cmd-a)

stash: key(cmd-s)
stash pop: key(cmd-shift-s)

^branch [<user.text>]:
    key(escape cmd-b)
    sleep(100ms)
    insert('{user.formatted_text(text or "", "DASH_SEPARATED")}')

^branch new [<user.text>]:
    key(escape cmd-shift-b)
    sleep(100ms)
    insert('{user.formatted_text(text or "", "DASH_SEPARATED")}')

^repo next: key(ctrl-tab)
^repo previous: key(shift-ctrl-tab)

^repo [<user.text>]:
    key(escape ctrl-cmd-p)
    insert('{user.formatted_text(text or "", "ALL_LOWERCASE,NO_SPACES")}')

^file previous: key(cmd-shift-[)
^file next: key(cmd-shift-])

^edit: key(cmd-enter)
