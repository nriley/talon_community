app: shrugs
-

tag(): user.messaging

# Sometimes a channel appears empty
channel reload: user.shrugs_channel_reload()

key(alt-shift-down): user.messaging_unread_next()
key(alt-shift-up): user.messaging_unread_previous()

key(alt-up): user.messaging_channel_previous()
key(alt-down): user.messaging_channel_next()
