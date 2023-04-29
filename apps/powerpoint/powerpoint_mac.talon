app: powerpoint_mac
-

# dictation mode gets confused when typing too fast
settings():
    insert_wait = 0.1

(slide | normal) view: key(cmd-1)
slide sorter: key(cmd-2)
notes page: key(cmd-3)
outline view: key(cmd-4)
reading view: key(cmd-5)
presenter view: key(esc alt-enter)

slideshow: key(cmd-enter)
slideshow from start: key(cmd-shift-enter)

slide new: key(cmd-shift-n)

slide hide: user.menu_select("Slide Show|Hide Slide")
slide unhide: user.menu_select("Slide Show|Unhide Slide")

align left: key(cmd-l)
align center: key(cmd-e)
align right: key(cmd-r)
align justify: key(cmd-j)

bold: key(cmd-b)
italic: key(cmd-i)
underline: key(cmd-u)

comment new: key(cmd-shift-m)

crop: key(shift-c)
guides: key(ctrl-cmd-alt-g)

bring to front: key(cmd-shift-f)
send to back: key(cmd-shift-b)

bring forward: key(cmd-alt-shift-f)
send backward: key(cmd-alt-shift-b)

group that: key(cmd-alt-g)
un group that: key(cmd-alt-shift-g)

copy style: key(cmd-shift-c)
paste style: key(cmd-shift-v)

mail this: user.menu_select("File|Share|Send Presentation")
mail p d f: user.menu_select("File|Share|Send PDF")

ribbon: key(cmd-alt-r)
ruler: user.menu_select("View|Ruler")

window (new | open): user.menu_select("Window|New Window")
