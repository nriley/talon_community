app: outlook_calendar_win
-
# moves by week
next: key(alt-down)
previous: key(alt-up)

tomorrow: key(ctrl-right)
yesterday: key(ctrl-left)
today: key(alt-h o d)

# XXX eliminate duplication with date_time.talon

# mm/0x
date <user.month> (o | zero) <digits>$:
    key(ctrl-g)
    insert("{month}/0{digits}")
    key(enter)

# mm/dd or mm/yy
date <user.month> <number_small>$:
    key(ctrl-g)
    insert("{month}/{number_small}")
    key(enter)

# mm/dd/0x
date <user.month> <user.day> (o | zero) <digits>$:
    key(ctrl-g)
    insert("{month}/{day}/0{digits}")
    key(enter)

# mm/dd/yy[yy]
date <user.month> <user.day> <user.year>:
    key(ctrl-g)
    insert("{month}/{day}/{year}")
    key(enter)
