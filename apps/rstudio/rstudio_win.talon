os: windows
app: rstudio
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
tag(): user.tabs

# XXX The below keyboard shortcuts were created by copying the Mac versions and replacing Command by Control.
# XXX Also, the actions invoked below need to be ported to Windows.

please [<user.text>]:
    key(ctrl-shift-p)
    insert(text or "")

(file | symbol) hunt [all] [<user.text>]:
    key(ctrl-.)
    sleep(200ms)
    user.paste(text or "")

run that: key(ctrl-enter)
run document: key(ctrl-alt-r)
run from top: key(ctrl-alt-b)
run to end: key(ctrl-alt-e)
run (function | funk): key(ctrl-alt-f)
run section: key(ctrl-alt-t)
run previous chunks: key(ctrl-alt-p)
run chunk: key(ctrl-alt-c)
run next chunk: key(ctrl-alt-n)
run all: key(ctrl-shift-s)
run knitter: key(ctrl-shift-k)
run profiler: key(ctrl-shift-alt-p)

# Moving around and formatting
go back: key(ctrl-f9)
go forward: key(ctrl-f10)
close all tabs: key(ctrl-shift-w)
indent lines: key(ctrl-i)
toggle comment: code.toggle_comment()
reformat comment: key(ctrl-shift-/)
reformat R code: key(ctrl-shift-a)
clone line up: key(ctrl-alt-up)
select to paren: key(ctrl-shift-e)
select to matching paren: key(ctrl-shift-alt-e)
jump to matching: key(ctrl-p)
expand selection: key(shift-alt-ctrl-up)
reduce selection: key(shift-alt-ctrl-down)
move active cursor up: key(ctrl-alt-shift-up)
move active cursor down: key(ctrl-alt-shift-down)

section next: key(ctrl-pagedown)
section previous: key(ctrl-pageup)

clear word left: key(alt-backspace)
clear word right: key(alt-delete)
assign that: key(alt--)
pipe that: key(ctrl-shift-m)
insert knitter chunk: key(ctrl-alt-i)

# Folding
fold that: key(ctrl-alt-l)
unfold that: key(ctrl-shift-alt-l)
fold all: key(ctrl-alt-o)
unfold all: key(ctrl-shift-alt-o)

# Find and replace
find with selection: key(ctrl-e)
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
go [to] section: key(ctrl-shift-alt-j)
go [to] tab: key(ctrl-shift-.)
go tab first: key(ctrl-shift-f11)

zoom source: key(ctrl-shift-1)
(zoom | show) all: key(ctrl-shift-0)

help that: key(f1)
(define that | go declaration | follow | definition show): key(f2)
previous plot: key(ctrl-alt-f11)
next plot: key(ctrl-alt-f12)

# devtools, package development, and session management
restart R session: key(ctrl-shift-f10)
dev tools build: key(ctrl-shift-b)
dev tools load all: key(ctrl-shift-l)
dev tools test: key(ctrl-shift-t)
dev tools check: key(ctrl-shift-e)
dev tools document: key(ctrl-shift-d)

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
# run and echo all:              key(ctrl-shift-enter)
# extract (function|funk):       key(ctrl-alt-x)
# extract variable:              key(ctrl-alt-v)
# new terminal:                  key(shift-alt-t)
# rename current terminal:       key(shift-alt-r)
# clear current terminal:        key(ctrl-shift-l)
# previous terminal:             key(ctrl-alt-f11)
# next terminal:                 key(ctrl-alt-f12)
# clear console:                 key(ctrl-l)
# popup history:                 key(ctrl-up)
# change working directory:      key(ctrl-shift-h)
# insert code section:           key(ctrl-shift-r)
# scroll diff view:              key(ctrl-up/down)
# sync editor & pdf preview:     key(ctrl-f8)
