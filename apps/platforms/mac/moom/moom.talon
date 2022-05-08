os: mac
-
# move window absolute
window top right: user.moom_keys('w')
window top left: user.moom_keys('q')
window bottom left: user.moom_keys('a')
window bottom right: user.moom_keys('s')
window center: user.moom_key('space')

# resize and move window
window fill left: user.moom_key('cmd-left')
window fill right: user.moom_key('cmd-right')
window fill top: user.moom_key('cmd-up')
window fill bottom: user.moom_key('cmd-down')

# resize window relative
window grow left [<user.ordinals>]: user.moom_keys('ctrl-left', ordinals or 1)
window grow right [<user.ordinals>]: user.moom_keys('ctrl-right', ordinals or 1)
window grow up [<user.ordinals>]: user.moom_keys('ctrl-up', ordinals or 1)
window grow down [<user.ordinals>]: user.moom_keys('ctrl-down', ordinals or 1)
window shrink left [<user.ordinals>]: user.moom_keys('alt-right', ordinals or 1)
window shrink right [<user.ordinals>]: user.moom_keys('alt-left', ordinals or 1)
window shrink top [<user.ordinals>]: user.moom_keys('alt-down', ordinals or 1)
window shrink bottom [<user.ordinals>]: user.moom_keys('alt-up', ordinals or 1)

# move window relative
window move left [<user.ordinals>]: user.moom_keys('left', ordinals or 1)
window move right [<user.ordinals>]: user.moom_keys('right', ordinals or 1)
window move up [<user.ordinals>]: user.moom_keys('up', ordinals or 1)
window move down [<user.ordinals>]: user.moom_keys('down', ordinals or 1)

# move window between screens
window screen up: user.moom_keys('-')
window screen down: user.moom_keys(';')
window screen left: user.moom_keys('o')
window screen right: user.moom_keys('p')

# undo after moving or resizing
window undo: user.moom_key('esc')
