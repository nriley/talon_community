app: keynote
-
tag(): user.pages

(slide | normal | navigator) view: user.menu_select("View|Navigator")
light table | slide sorter: user.menu_select("View|Light Table")
outline view: user.menu_select("View|Outline")
presenter view | rehearse slideshow: key(cmd-alt-r)

slide layouts | master slide: key(cmd-shift-e)

slideshow: key(cmd-alt-p)

[slide] previous: user.page_previous()
[slide] next: user.page_next()
[slide] final: user.page_final()

slide new: key(cmd-shift-n)

slide (hide | unhide): key(cmd-shift-h)

align left: key(cmd-{)
align center: key(cmd-|)
align right: key(cmd-})
align justify: key(cmd-alt-|)

bold: key(cmd-b)
italic: key(cmd-i)
underline: key(cmd-u)

comment new: key(cmd-shift-k)

crop | mask: key(cmd-shift-m)

bring to front: key(cmd-shift-f)
send to back: key(cmd-shift-b)

bring forward: key(cmd-alt-shift-f)
send backward: key(cmd-alt-shift-b)

group that: key(cmd-alt-g)
un group that: key(cmd-alt-shift-g)

toolbar: key(cmd-alt-t)
ruler: key(cmd-r)
