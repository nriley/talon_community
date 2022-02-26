app: excel_mac
-
tag(): user.find_and_replace

save as excel: user.excel_save_as_format('Excel Workbook (.xlsx)')

fill down: key(cmd-d)
fill right: key(cmd-r)
insert that: key(ctrl-shift-=)
delete that: key(cmd--)

paste special: key(cmd-ctrl-v)

align left: key(cmd-l)
align center: key(cmd-e)

filter: key(cmd-shift-f)
sort: key(cmd-shift-r)
table: key(cmd-t)

formula: key(shift-f3)
reference: key(cmd-t)

edit: key(ctrl-u)
complete: key(alt-down)
ditto: key(ctrl-shift-')

bold: key(cmd-b)
italic: key(cmd-i)
underline: key(cmd-u)
strike through: key(cmd-shift-x)

format general: key(ctrl-~)
format currency: key(ctrl-$)
format (percent | percentage): key(ctrl-%)
format decimal: key(ctrl-!)
format exponential: key(ctrl-^)
format date: key(ctrl-#)
format time: key(ctrl-@)

cell border: key(cmd-alt-0)
cell border left: key(cmd-alt-left)
cell border right: key(cmd-alt-right)
cell border top: key(cmd-alt-up)
cell border bottom: key(cmd-alt-down)
cell border clear: key(cmd-alt--)

cell select: key(shift-backspace)
cell note: key(shift-f2)
cell comment: key(cmd-shift-f2)
cell name: key(cmd-f3)
cell menu: key(shift-f10)

array select: key(ctrl-/)

column hide: key(ctrl-0)
column unhide: key(ctrl-shift-0)
column select: key(ctrl-space)
column insert: key(ctrl-space ctrl-shift-=)
column delete: key(ctrl-space cmd--)
column top: key(cmd-up)
column bottom: key(cmd-down)
column fit: user.menu_select('Format|Column|AutoFit Selection')
column filter: key(cmd-down cmd-up alt-down)
column width: user.menu_select('Format|Column|Width...')

row hide: key(ctrl-9)
row unhide: key(ctrl-shift-9)
row select: key(shift-space)
row insert: key(shift-space ctrl-shift-=)
row delete: key(shift-space cmd--)
row start: key(cmd-left)
row end: key(cmd-right)
row fit: user.menu_select('Format|Row|AutoFit')
row height: user.menu_select('Format|Row|Height...')

table select: key(cmd-a)
select all: key(cmd-a cmd-a cmd-a)

sheet new: key(shift-f11)
sheet previous: key(alt-left)
sheet next: key(alt-right)

ribbon: key(cmd-alt-r)

window (new|open): user.menu_select('Window|New Window')
