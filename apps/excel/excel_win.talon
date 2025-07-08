app: excel_win
-
# tag(): user.find_and_replace

save as excel: user.excel_save_as_format("Excel Workbook (*.xlsx)")
password: user.office_win_ribbon_select("fipe")

fill down: key(ctrl-d)
fill right: key(ctrl-r)
insert that: key(ctrl-shift-=)
delete that: key(ctrl--)

paste special: key(ctrl-alt-v)

align left: user.office_win_ribbon_select("hal")
align center: user.office_win_ribbon_select("hac")
align right: user.office_win_ribbon_select("har")

# filter: key(cmd-shift-f)
# sort: key(cmd-shift-r)
table: key(ctrl-t)

formula: key(shift-f3)
# reference: key(cmd-t)

edit: key(f2)
complete: key(alt-down)
ditto: key(ctrl-shift-')
bold: key(ctrl-b)
italic: key(ctrl-i)
underline: key(ctrl-u)
# strike through: key(cmd-shift-x)

# format general: key(ctrl-~)
# format currency: key(ctrl-$)
# format (percent | percentage): key(ctrl-%)
# format (decimal | number): key(ctrl-!)
# format exponential: key(ctrl-^)
# format date: key(ctrl-#)
# format time: key(ctrl-@)

# cell border: key(cmd-alt-0)
# cell border left: key(cmd-alt-left)
# cell border right: key(cmd-alt-right)
# cell border top: key(cmd-alt-up)
# cell border bottom: key(cmd-alt-down)
# clear cell border: key(cmd-alt--)

# cell select: key(shift-backspace)
cell note: key(shift-f2)
cell comment: key(ctrl-shift-f2)
cell name: key(alt-f3)
cell menu: key(shift-f10)

# array select: key(ctrl-/)

column hide: key(ctrl-0)
# column unhide: key(ctrl-shift-0)
column select: key(ctrl-space)
column insert: key(ctrl-space ctrl-shift-=)
column delete: key(ctrl-space ctrl--)
column top: key(ctrl-up)
column bottom: key(ctrl-down)
column fit: user.office_win_ribbon_select("hoi")
column filter: key(ctrl-down ctrl-up alt-down)
column width: user.office_win_ribbon_select("how")

row hide: key(ctrl-9)
# row unhide: key(ctrl-shift-9)
row select: key(shift-space)
row insert: key(shift-space ctrl-shift-=)
row delete: key(shift-space ctrl--)
row start: key(ctrl-left)
row end: key(ctrl-right)
row fit: user.office_win_ribbon_select("hoa")
row height: user.office_win_ribbon_select("hoh")

table select: key(ctrl-a)
select all: key(ctrl-a:3)

sheet new: key(shift-f11)
sheet previous: key(ctrl-pageup)
sheet next: key(ctrl-pagedown)
sheet rename: user.office_win_ribbon_select("hor")

pivot that: user.office_win_ribbon_select("nvt")
mail this: user.office_mail_this()

ribbon: key(ctrl-f1)

(select | take | go [to]) <user.excel_reference>:
    key(ctrl-g)
    insert(excel_reference)
    key(return)
