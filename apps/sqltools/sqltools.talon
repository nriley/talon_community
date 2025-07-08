app: sqltools
-
tag(): user.line_commands
tag(): user.tabs

connect: key(ctrl-d c)
reconnect: key(ctrl-d e)
cache refresh: key(alt-o o enter)

run: key(ctrl-enter)
explain plan: key(f9)
quick query: key(f11)
object: key(f12)
object script: key(ctrl-f12)
sequel plus: key(ctrl-shift-f5)

# Intentional overlap with formatting commands
all cap that: key(ctrl-shift-up)
all down that: key(ctrl-shift-down)
title that: key(ctrl-k a)
norm that: key(ctrl-k n)

bar switch: key(alt-0)

result: user.sqltools_select_pane("Result")
statistics: user.sqltools_select_pane("Statistics")
plan: user.sqltools_select_pane("Plan")
output: user.sqltools_select_pane("Output")
history: user.sqltools_select_pane("History")
binds: user.sqltools_select_pane("Binds")

open: user.sqltools_click_button("Open with default CSV viewer...")
