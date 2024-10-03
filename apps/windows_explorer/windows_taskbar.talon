os: windows
-
# update to Win+N in Windows 11
^calendar mini:
    key("super-b")
    sleep(50ms)
    key("left:2 enter")

proxy toggle: user.click_taskbar_button("IE proxy disabled|IE proxy enabled")
