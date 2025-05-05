os: windows
-
# not universal but common enough
app (exit | quit): key(alt-f x)
full screen: key(f11)
window maximize: user.window_maximize()
window restore: user.window_restore()
refresh: key(f5)

# Windows logo key shortcuts
^(action | note | notification) center$: key(super-a)
launch paste: key(super-v)
