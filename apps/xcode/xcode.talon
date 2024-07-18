app: xcode
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.splits
tag(): user.tabs

file hunt [<user.text>]:
    key(cmd-shift-o)
    insert(text or "")

product run: key(cmd-r)
product stop: key(cmd-.)
product build: key(cmd-b)
product archive: user.menu_select("Product|Archive")

product clean: key(cmd-shift-k)

organizer: key(cmd-shift-alt-o)

# Sidebar navigators (left side)
bar (project | explore): key(cmd-1)
bar source: key(cmd-2)
bar symbols: key(cmd-3)
bar (find | search): key(cmd-4)
bar issues: key(cmd-5)
bar test: key(cmd-6)
bar debug: key(cmd-7)
bar breakpoints: key(cmd-8)
bar switch: key(cmd-0)

# Inspectors (right side)
inspect file: key(cmd-alt-1)
inspect history: key(cmd-alt-2)
inspect help: key(cmd-alt-3)
inspect switch: key(cmd-alt-0)

# Debug area (bottom)
bug switch: key(cmd-shift-y)
bug console: key(cmd-shift-c)

# Navigate
focus next: key(cmd-alt-`)
focus previous: key(cmd-alt-shift-`)
focus pick: key(cmd-j)
go forward: key(ctrl-cmd-right)
go back: key(ctrl-cmd-left)
(go definition | follow): key(cmd-ctrl-j)
issue next: key(cmd-')
issue previous: key(cmd-")
counterpart next: key(cmd-ctrl-up)
counterpart previous: key(cmd-ctrl-down)
