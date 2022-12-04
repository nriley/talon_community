os: mac
and app.bundle: 85C27NK92C.com.flexibits.fantastical2.mac.helper
os: mac
and app.bundle: com.flexibits.fantastical2.mac
-
next: key(cmd-right)
previous: key(cmd-left)
today: key(cmd-t)

calendar set [<user.text>]: user.fantastical_select_calendar_set(text or "")

toggle sidebar: key(cmd-alt-s)

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
