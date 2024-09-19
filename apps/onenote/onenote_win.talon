app: onenote_win
-
refresh: key(ctrl-pagedown ctrl-pageup)

bold: key(ctrl-b)
italic: key(ctrl-i)
strike through: key(ctrl--)
# The below commented action implementation should work fine for most people.
# I have bound Ctrl+Alt+H to a Talon action so I can't use it.
# highlight: key(ctrl-alt-h)
highlight:
    user.office_win_ribbon_select("hi")
    key(enter)

font size [<number_small>]: user.onenote_font_size(number_small or 0)
(bigger | larger): key(ctrl-shift->)
smaller: key(ctrl-shift-<)

align left: key(ctrl-l)
align right: key(ctrl-r)

bullet: key(ctrl-.)
check | done: key(ctrl-1)
tag clear: key(ctrl-0)

insert date: key(alt-shift-d)

heading one: key(ctrl-alt-1)
heading two: key(ctrl-alt-2)
normal: key(ctrl-shift-n)

code:
    key(ctrl-shift-n)
    user.office_win_ribbon_select("hl")
    key(up:3 enter)

move up: key(alt-shift-up)
move down: key(alt-shift-down)
move right: key(alt-shift-right)
move left: key(alt-shift-left)

cell select: user.office_win_ribbon_select("jc")

column select: user.office_win_ribbon_select("jm")
column insert left: user.office_win_ribbon_select("jl")
column insert right: key(ctrl-alt-r)
column delete: user.office_win_ribbon_select("ju")

row select: user.office_win_ribbon_select("jo")
row insert up: user.office_win_ribbon_select("jv")
row insert down: user.office_win_ribbon_select("je")
row delete: user.office_win_ribbon_select("jw")

table select: user.office_win_ribbon_select("js")

# for consistency with Mac version, where collapsing will collapse to level 1
collapse: key(alt-shift-1)
expand [this | that]: key(alt-shift-+)
expand all: key(alt-shift-0)

# but add option to just collapse a single level
collapse (this | that): key(alt-shift--)

mail this: user.office_win_ribbon_select("hm1")

go (notebook | notebooks): key(ctrl-g)

go (section | sections): key(ctrl-shift-g)
section previous: key(ctrl-shift-tab)
section next: key(ctrl-tab)

go (page | pages): key(ctrl-alt-g)
page new: key(ctrl-n)
page delete: key(ctrl-alt-g delete)
page previous: key(ctrl-pageup)
page next: key(ctrl-pagedown)
page move right: key(ctrl-alt-g shift-f10 s)
page move left: key(ctrl-alt-g shift-f10 o enter)

(page | name) date [<user.prose>]$:
    key(ctrl-shift-t alt-shift-d)
    user.insert_formatted(prose or "", "CAPITALIZE_FIRST_WORD")

[page] name [<user.prose>]$:
    key(ctrl-shift-t)
    user.insert_formatted(prose or "", "CAPITALIZE_FIRST_WORD")

go forward: key(alt-right)
go back: key(alt-left)

[open] link: key(shift-f10 l)
edit link: key(ctrl-k)
copy link: key(shift-f10 p)
paste link: key(ctrl-k alt-e ctrl-v enter)
remove link: key(shift-f10 r)

# not standard OneNote; triggers an AutoHotKey macro I wrote
today: key(super-alt-d)

tomorrow:
    key(super-alt-shift-d)
    sleep(300ms)
    key(1)

<digit_string> days:
    key(super-alt-shift-d)
    sleep(300ms)
    insert(digit_string)

# back to progress (first notebook, first section)
go progress: user.onenote_go_progress()

# Windows+arrows do not work in full screen mode
window minimize: key(alt-space n)
window maximize: key(alt-space x)
