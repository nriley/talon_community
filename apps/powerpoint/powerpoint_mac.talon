app: powerpoint_mac
-

tag(): user.pages

settings():
    # always paste to insert
    user.paste_to_insert_threshold = 0
    # wait longer before insertion to prevent incorrect insertion in the middle of text
    user.insert_wait = 5

(slide | normal) view: key(cmd-1)
slide sorter: key(cmd-2)
notes page: key(cmd-3)
outline view: key(cmd-4)
reading view: key(cmd-5)
presenter view: key(esc alt-enter)

master slide: key(cmd-alt-1)
master handout: key(cmd-alt-2)
master notes: key(cmd-alt-3)

slideshow: key(cmd-enter)
slideshow from start: key(cmd-shift-enter)

[slide] previous: user.page_previous()
[slide] next: user.page_next()
[slide] final: user.page_final()

slide new: key(cmd-shift-n)

slide hide: user.menu_select("Slide Show|Hide Slide")
slide unhide: user.menu_select("Slide Show|Unhide Slide")

# text alignment
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

# object alignment and distribution
align these left: user.menu_select("Arrange|Align or Distribute|Align Left")
align these center: user.menu_select("Arrange|Align or Distribute|Align Center")
align these right: user.menu_select("Arrange|Align or Distribute|Align Right")
align these top: user.menu_select("Arrange|Align or Distribute|Align Top")
align these middle: user.menu_select("Arrange|Align or Distribute|Align Middle")
align these bottom: user.menu_select("Arrange|Align or Distribute|Align Bottom")
distribute these horizontally:
    user.menu_select("Arrange|Align or Distribute|Distribute Horizontally")
distribute these vertically:
    user.menu_select("Arrange|Align or Distribute|Distribute Vertically")

reorder that: user.menu_select("Arrange|Reorder Objects")
group that: key(cmd-alt-g)
un group that: key(cmd-alt-shift-g)
regroup that: key(cmd-alt-j)

(copy | pick up object) style: key(cmd-shift-c)
(pace | pist | paste | apply object) style | pistil: key(cmd-shift-v)
duplicate: key(cmd-d)

mail this: user.menu_select("File|Share|Send Presentation")
mail p d f: user.menu_select("File|Share|Send PDF")

ribbon: key(cmd-alt-r)
ruler: user.menu_select("View|Ruler")
pane selection: key(cmd-alt-u)
pane (format | object): key(cmd-shift-1)
