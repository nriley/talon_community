app: powerpoint_win
-

(slide | normal) view: user.office_win_ribbon_select("wl")
slide sorter: user.office_win_ribbon_select("wi")
notes page: user.office_win_ribbon_select("wt")
outline view: user.office_win_ribbon_select("wpo")
reading view: user.office_win_ribbon_select("wd")
presenter view: key(alt-f5)

slideshow: key(f5)
slideshow from start: user.office_win_ribbon_select("sb")

slide previous: key(f6 escape:2 pageup)
slide next: key(f6 escape:2 pagedown)

slide new: key(ctrl-m)

# Can't get this to work reliably from keyboard commands
# Would likely need to do via accessibility/COM
# slide (hide|unhide): key(f6 escape:2 shift-f10 h:2)

align left: key(ctrl-l)
align center: key(ctrl-e)
align right: key(ctrl-r)
align justify: key(ctrl-j)

bold: key(ctrl-b)
italic: key(ctrl-i)
underline: key(ctrl-u)

comment new: key(ctrl-alt-m)

# crop: key(shift-c)
guides: key(alt-f9)

bring to front: key(ctrl-shift-])
send to back: key(ctrl-shift-[)

bring forward: key(ctrl-])
send backward: key(ctrl-[])

group that: key(ctrl-g)
un group that: key(ctrl-shift-g)

copy style: key(ctrl-shift-c)
(pace | pist | paste) style: key(ctrl-shift-v)

mail this:
    user.office_tell_me()
    "Mail Recipient (As Attachment)"
    sleep(1s)
    key(down enter)

mail p d f:
    user.office_tell_me()
    "E-mail as PDF Attachment"
    sleep(1s)
    key(down enter)

ribbon: key(ctrl-f1)
ruler: user.office_win_ribbon_select("wr")
