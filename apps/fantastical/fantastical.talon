app: fantastical
-

next: key(cmd-right)
previous: key(cmd-left)
tomorrow: key(shift-right)
yesterday: key(shift-left)
today: key(cmd-t)

day view: key(cmd-1)
week view: key(cmd-2)
month view: key(cmd-3)
quarter view: key(cmd-4)
year view: key(cmd-5)

calendar set [<user.text>]: user.fantastical_select_calendar_set(text or "")

bar switch: key(cmd-alt-s)

pending: user.fantastical_show_notifications()
pending dismiss: user.fantastical_clear_all_notifications()

dismiss: key(cmd-enter down)
accept: key(cmd-alt-1 down)
maybe: key(cmd-alt-2 down)
decline: key(cmd-alt-3 down)

# XXX eliminate duplication with date_time.talon

# mm/0x
date <user.month> (o | zero) <digits>$:
    key(cmd-shift-t)
    insert("{month}/0{digits}")
    key(enter)

# mm/dd or mm/yy
date <user.month> <number_small>$:
    key(cmd-shift-t)
    insert("{month}/{number_small}")
    key(enter)

# mm/dd/0x
date <user.month> <user.day> (o | zero) <digits>$:
    key(cmd-shift-t)
    insert("{month}/{day}/0{digits}")
    key(enter)

# mm/dd/yy[yy]
date <user.month> <user.day> <user.year>:
    key(cmd-shift-t)
    insert("{month}/{day}/{year}")
    key(enter)
