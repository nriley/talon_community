app: putty
app: citrix_desktop
-
session menu: user.putty_open_menu()

session new:
    user.putty_open_menu()
    "w"

session (duplicate | dupe):
    user.putty_open_menu()
    "d"

session saved:
    user.putty_open_menu()
    "v"

session clear:
    user.putty_open_menu()
    "t"
    sleep(200ms)
    user.putty_open_menu()
    "l"

session copy:
    user.putty_open_menu()
    "o"

session restart:
    user.putty_open_menu()
    "r"
