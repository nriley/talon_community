app: omnioutliner
-

move up: key(cmd-ctrl-up)
move down: key(cmd-ctrl-down)
move right: key(cmd-ctrl-right)
move left: key(cmd-ctrl-left)

# everything
expand all: key(ctrl-cmd-9)
collapse all: key(ctrl-cmd-0)

# all subheadings ("completely")
expand: key(cmd-alt-9)
collapse: key(cmd-alt-0)

# single level
expand that: key(cmd-9)
collapse that: key(cmd-0)

focus | hoist: key(cmd-shift-f)
unfocused | unhoist: key(cmd-shift-alt-f)

toolbar: key(cmd-alt-t)
# status bar

bar switch: key(cmd-alt-1)
bar sections: user.menu_select("View|Sidebar|Sections")
bar styles: user.menu_select("View|Sidebar|Styles")
bar find: user.menu_select("View|Sidebar|Batch Find")
bar filters: user.menu_select("View|Sidebar|Filters")

inspector | sec switch: key(cmd-shift-i)
