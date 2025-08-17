os: windows
-
^calendar mini:
    key("super-n")
    sleep(50ms)
    key("left:2 enter")

proxy toggle:
    user.click_system_tray_button("IEProxyToggle.exe IE proxy disabled|IEProxyToggle.exe IE proxy enabled")
