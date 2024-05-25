app: onenote_mac
-
tag(): user.find_and_replace

# due to a combination of clipboard slowness/flakiness, issues with inserting text in tables
# and lack of exposure though accessibility
settings():
    user.context_sensitive_dictation = 0
    insert_wait = 1

bold: key(cmd-b)
italic: key(cmd-i)
strike through: key(ctrl-cmd--)
highlight: key(ctrl-cmd-h)

font [<user.text>]: user.onenote_font('{text or ""}')
font size [<number_small>]: user.onenote_font_size(number_small or 0)
(bigger | larger): user.onenote_font_size_adjust(1)
smaller: user.onenote_font_size_adjust(-1)

align left: key(cmd-l)
align right: key(cmd-r)

bullet: key(cmd-.)
check | done: key(cmd-1)
tag remove: key(cmd-alt-0)

insert date: key(cmd-d)

heading one: key(cmd-alt-1)
heading two: key(cmd-alt-2)
normal: key(cmd-shift-n)
code: user.menu_select("Format|Styles|Code")

move up: key(cmd-alt-up)
move down: key(cmd-alt-down)
move right: key(cmd-])
move left: key(cmd-[)

cell select: user.menu_select("Format|Table|Select Cell")

column select: user.menu_select("Format|Table|Select Columns")
column insert left: key(cmd-ctrl-l)
column insert right: key(cmd-ctrl-r)
column delete: user.menu_select("Format|Table|Delete Columns")

row select: user.menu_select("Format|Table|Select Rows")
row insert up: user.menu_select("Format|Table|Insert Rows Above")
row insert down: key(cmd-enter)
row delete: user.menu_select("Format|Table|Delete Rows")

table select: user.menu_select("Format|Table|Select Table")

collapse: key(ctrl-shift--)
expand: key(ctrl-shift-+)

# just collapse a single level
collapse (this | that): user.onenote_collapse_this()

ribbon: key(cmd-alt-r)

mail this: user.menu_select("File|Share|Send Page as Email Message")

go (notebook | notebooks): key(ctrl-g)
go notebook <user.onenote_notebook>:
    user.onenote_navigate(onenote_notebook)
    key(enter)

go (section | sections): key(ctrl-shift-g)
go section <user.onenote_section>: user.onenote_navigate(onenote_section)
section new: key(cmd-t)
section previous: key(cmd-{)
section next: key(cmd-})

go (page | pages): key(ctrl-cmd-g)
go page <user.onenote_page>: user.onenote_navigate(onenote_page)
page new:
    key(cmd-n)
    sleep(100ms)
page delete: key(ctrl-cmd-g cmd-delete)
page previous: key(ctrl-cmd-g up tab)
page next: key(ctrl-cmd-g down tab)
page move up: key(ctrl-cmd-g cmd-alt-up)
page move down: key(ctrl-cmd-g cmd-alt-down)
page move right: key(cmd-alt-])
page move left: key(cmd-alt-[)

(page | name) date [<user.prose>]$:
    key(cmd-shift-t cmd-d)
    sleep(200ms)
    insert(prose or "")

[page] name [<user.prose>]$:
    key(cmd-shift-t)
    sleep(100ms)
    user.insert_formatted(prose or "", "CAPITALIZE_FIRST_WORD")

# navigating in notebook/section/page lists
go top: key(alt-up)
go bottom: key(alt-down)

# navigating in recent notes (pages)
page forward [<user.ordinals>]$:
    offset = ordinals or 1
    offset = -1 * offset
    user.onenote_go_recent(offset)

page back [<user.ordinals>]$: user.onenote_go_recent(ordinals or 1)

key(cmd-ctrl-down): user.onenote_go_recent(1)
key(cmd-ctrl-up): user.onenote_go_recent(-1)

# navigating by cursor position
go forward: key(cmd-ctrl-right)
go back: key(cmd-ctrl-left)

[open] link: key(left right:2 enter)
edit link: key(cmd-k)
copy link: user.onenote_copy_link()
key(cmd-ctrl-c): user.onenote_copy_link()

paste link:
    key(cmd-k)
    sleep(100ms)
    key(cmd-v)
    sleep(100ms)
    key(enter cmd-shift-n)

# missing shortcut for hiding navigation
(navigation hide | escape):
    user.onenote_hide_ribbon()
    user.onenote_hide_navigation()
    user.zoom_to_fit_width()

key(esc):
    user.onenote_hide_ribbon()
    user.onenote_hide_navigation()
    user.zoom_to_fit_width()

today:
    user.onenote_heading_1()
    key(cmd-d)
    insert("- ")
    key(up ctrl-shift--)
    sleep(500ms)
    key(down)
    user.onenote_checkbox()

key(ctrl-cmd-t): mimic("today")

tomorrow:
    user.onenote_heading_1()
    user.insert_date(1, "%-m/%-d/%Y")
    insert(" - ")
    key(up ctrl-shift--)
    sleep(500ms)
    key(down)
    user.onenote_checkbox()

# back to progress (first notebook, first section)
go progress:
    user.onenote_go_progress()
    user.onenote_hide_ribbon()
    user.onenote_hide_navigation()
    user.zoom_to_fit_width()
