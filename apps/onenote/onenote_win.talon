os: windows
and app.exe: ONENOTE.EXE
-
refresh: key(ctrl-pagedown ctrl-pageup)

bold: key(ctrl-b)
italic: key(ctrl-i)
strike through: key(ctrl--)
highlight: key(ctrl-alt-h)

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
    key(ctrl-shift-n alt-h)
    sleep(50ms)
    key(alt-l up enter)

move up: key(alt-shift-up)
move down: key(alt-shift-down)
move right: key(alt-shift-right)
move left: key(alt-shift-left)

cell select: user.onenote_ribbon_select("jlc")

column select: user.onenote_ribbon_select("jlm")
column insert left: user.onenote_ribbon_select("jll")
column insert right: key(ctrl-alt-r)
column delete: user.onenote_ribbon_select("jlu")

row select: user.onenote_ribbon_select("jlo")
row insert up: user.onenote_ribbon_select("jlv")
row insert down: user.onenote_ribbon_select("jle")
row delete: user.onenote_ribbon_select("jlw")

table select: user.onenote_ribbon_select("jls")

# for consistency with Mac version, where collapsing will collapse to level 1
collapse: key(alt-shift-1)
expand [this | that]: key(alt-shift-+)
expand all: key(alt-shift-0)

# but add option to just collapse a single level
collapse (this | that): key(alt-shift--)

mail this: user.onenote_ribbon_select("hm1")

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

[page] rename date [<user.prose>]$:
    key(ctrl-shift-t alt-shift-d)
    user.insert_formatted(prose or "", "CAPITALIZE_FIRST_WORD")

[page] rename [<user.prose>]$:
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
go progress: key(ctrl-g home enter tab:3 down enter esc)

# Windows+arrows do not work in full screen mode
window minimize: key(alt-space n)
window maximize: key(alt-space x)
