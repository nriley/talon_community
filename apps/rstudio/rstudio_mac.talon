os: mac
app: rstudio
-
tag(): user.command_search
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
tag(): user.tabs

(file | symbol) hunt [all] [<user.text>]:
    key(ctrl-.)
    sleep(200ms)
    user.paste(text or "")

run that: key(cmd-enter)
run document: key(cmd-alt-r)
run from top: key(cmd-alt-b)
run to end: key(cmd-alt-e)
run (function | funk): key(cmd-alt-f)
run section: key(cmd-alt-t)
run previous chunks: key(cmd-alt-p)
run chunk: key(cmd-alt-c)
run next chunk: key(cmd-alt-n)
run all: key(cmd-shift-s)
run knitter: key(cmd-shift-k)
run profiler: key(cmd-shift-alt-p)

# Moving around and formatting
jump back:
    app.notify('ERROR: Command deprecated; please use "go back"')
    key(cmd-f9)
go back: key(cmd-f9)
jump forward:
    app.notify('ERROR: Command deprecated; please use "go forward"')
    key(cmd-f10)
go forward: key(cmd-f10)
close all tabs: key(cmd-shift-w)
indent lines: key(cmd-i)
toggle comment: code.toggle_comment()
reformat comment: key(cmd-shift-/)
reformat R code: key(cmd-shift-a)
line up:
    app.notify('ERROR: Command deprecated; please use "drag up"')
    edit.line_swap_up()
line down:
    app.notify('ERROR: Command deprecated; please use "drag down"')
    edit.line_swap_down()
duplicate line up:
    app.notify('ERROR: Command deprecated; please use "clone line up"')
    key(cmd-alt-up)
clone line up: key(cmd-alt-up)
duplicate line [down]:
    app.notify('ERROR: Command deprecated; please use "clone line"')
    edit.line_clone()
select to paren: key(ctrl-shift-e)
select to matching paren: key(ctrl-shift-alt-e)
jump to matching: key(ctrl-p)
expand selection: key(shift-alt-cmd-up)
reduce selection: key(shift-alt-cmd-down)
add cursor up:
    app.notify('ERROR: Command deprecated; please use "cursor up"')
    user.multi_cursor_add_above()
    key(ctrl-alt-up)
add cursor down:
    app.notify('ERROR: Command deprecated; please use "cursor down"')
    user.multi_cursor_add_below()
    key(ctrl-alt-down)
move active cursor up: key(ctrl-alt-shift-up)
move active cursor down: key(ctrl-alt-shift-down)
delete line:
    app.notify('ERROR: Command deprecated; please use "clear line"')
    edit.delete_line()
    key(cmd-d)

section next: key(cmd-pagedown)
section previous: key(cmd-pageup)

delete word left:
    app.notify('ERROR: Command deprecated; please use "clear word left"')
    key(alt-backspace)
clear word left: key(alt-backspace)
delete word right:
    app.notify('ERROR: Command deprecated; please use "clear word right"')
    key(alt-delete)
clear word right: key(alt-delete)
assign that: key(alt--)
pipe that: key(cmd-shift-m)
[insert knitter] chunk: key(cmd-alt-i)

# Folding
fold that: key(cmd-alt-l)
unfold that: key(cmd-shift-alt-l)
fold all: key(cmd-alt-o)
unfold all: key(cmd-shift-alt-o)

# Find and replace
find and replace:
    app.notify('ERROR: Command deprecated; please use "hunt this"')
    edit.find("")
find next:
    app.notify('ERROR: Command deprecated; please use "hunt next"')
    edit.find_next()
find previous:
    app.notify('ERROR: Command deprecated; please use "hunt previous"')
    edit.find_previous()
find with selection: key(cmd-e)
find in files:
    app.notify('ERROR: Command deprecated; please use "hunt all"')
    user.find_everywhere("")
run replace:
    app.notify('ERROR: Command deprecated; please use "replace confirm that"')
    user.replace_confirm()
run spell check: key(f7)

# Navigation and panels
go [to] source: key(ctrl-1)
go [to] console: key(ctrl-2)
go [to] help: key(ctrl-3)
go [to] history: key(ctrl-4)
go [to] files: key(ctrl-5)
go [to] (plots | plot): key(ctrl-6)
go [to] packages: key(ctrl-7)
go [to] environment: key(ctrl-8)
go [to] git: key(ctrl-9)
go [to] build: key(ctrl-0)
go [to] terminal: key(alt-shift-t)
go [to] omni: key(ctrl-.)
go to line:
    app.notify('ERROR: Command deprecated; please use "go <number>"')
    key(cmd-shift-alt-g)
go [to] section: key(cmd-shift-alt-j)
go [to] tab: key(ctrl-shift-.)
go to previous tab:
    app.notify('ERROR: Command deprecated; please use "tab (last | previous)"')
    app.tab_previous()
go to next tab:
    app.notify('ERROR: Command deprecated; please use "tab next"')
    app.tab_next()
go to first tab:
    app.notify('ERROR: Command deprecated; please use "go tab first"')
    key(ctrl-shift-f11)
go tab first: key(ctrl-shift-f11)
go to last tab:
    app.notify('ERROR: Command deprecated; please use "go tab final"')
    user.tab_final()

zoom source: key(ctrl-shift-1)
(zoom | show) all: key(ctrl-shift-0)

help that: key(f1)
(define that | go declaration | follow | definition show): key(f2)
previous plot: key(cmd-alt-f11)
next plot: key(cmd-alt-f12)

# devtools, package development, and session management
restart R session: key(cmd-shift-f10)
dev tools build: key(cmd-shift-b)
dev tools load all: key(cmd-shift-l)
dev tools test: key(cmd-shift-t)
dev tools check: key(cmd-shift-e)
dev tools document: key(cmd-shift-d)

# Debugging
# XXX user.debugger
toggle breakpoint: key(shift-f9)
debug next: key(f10)
debug step into (function | funk): key(shift-f4)
debug finish (function | funk): key(shift-f6)
debug continue: key(shift-f5)
debug stop: key(shift-f8)

# Git/SVN
run git diff: key(ctrl-alt-d)
run git commit: key(ctrl-alt-m)

# Other shortcuts that could be enabled
# run line and stay:             key(alt-enter)
# run and echo all:              key(cmd-shift-enter)
# extract (function|funk):       key(cmd-alt-x)
# extract variable:              key(cmd-alt-v)
# new terminal:                  key(shift-alt-t)
# rename current terminal:       key(shift-alt-r)
# clear current terminal:        key(ctrl-shift-l)
# previous terminal:             key(ctrl-alt-f11)
# next terminal:                 key(ctrl-alt-f12)
# clear console:                 key(ctrl-l)
# popup history:                 key(cmd-up)
# change working directory:      key(ctrl-shift-h)
# insert code section:           key(cmd-shift-r)
# scroll diff view:              key(ctrl-up/down)
# sync editor & pdf preview:     key(cmd-f8)
