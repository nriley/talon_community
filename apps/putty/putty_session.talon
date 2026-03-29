app: putty
app: citrix_desktop_mac
-

session menu: user.putty_open_menu()

session new:
    user.putty_open_menu()
    insert("w")

session (duplicate | dupe):
    user.putty_open_menu()
    insert("d")

session saved:
    user.putty_open_menu()
    insert("v")

session clear:
    user.putty_open_menu()
    insert("t")
    sleep(200ms)
    user.putty_open_menu()
    insert("l")

session copy:
    user.putty_open_menu()
    insert("o")

session restart:
    user.putty_open_menu()
    insert("r")
