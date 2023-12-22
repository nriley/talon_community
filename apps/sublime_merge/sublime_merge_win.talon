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

# navigate to first hunk in file (or section in Summary tab)
hunk:
    key(ctrl-pagedown ctrl-pageup)
    sleep(150ms)
    key(tab)

go locations: key(ctrl-1)
go commits: key(ctrl-2)
go files: key(ctrl-3)

commit: key(ctrl-9 ctrl-enter)
push: key(ctrl-alt-up)
push force:
    key(shift-f8)
    "--force-with-lease"
    key(enter)
pull: key(ctrl-alt-down)

# stage commands work when insertion point is in a hunk

# this tends to get preferred to other stage commands (and can be destructive to your carefully curated
# commit); feel free to uncomment if you don't see the conflict
# ^stage | unstage$: key(shift-enter)

(stage | unstage) (this | hunk | lines): key(enter)

# stage command works in a file tab
file (stage | unstage):
    key(ctrl-pageup ctrl-pagedown)
    sleep(100ms)
    key(tab shift-enter)

stage all:
    key(ctrl-shift-a)
    sleep(100ms)
unstage all: key(ctrl-shift-r)
stage untracked: key(ctrl-k ctrl-a)

stash: key(ctrl-s)
stash pop: key(ctrl-shift-s)

^branch [<user.text>]:
    key(escape ctrl-b)
    insert('{user.formatted_text(text or "", "ALL_LOWERCASE,NO_SPACES")}')

^branch new [<user.text>]:
    key(escape ctrl-shift-b)
    sleep(100ms)
    insert('{user.formatted_text(text or "", "DASH_SEPARATED")}')

^repo next: key(ctrl-tab)
^repo previous: key(shift-ctrl-tab)

^repo [<user.text>]:
    key(ctrl-shift-o)
    insert('{user.formatted_text(text or "", "ALL_LOWERCASE,NO_SPACES")}')

^file previous: key(ctrl-pageup)
^file next: key(ctrl-pagedown)

# works only when a file/hunk is focused
^edit: key(ctrl-enter)
    
# Win+down x2 does not reliably minimize the window
window minimize: key(alt-space n)
