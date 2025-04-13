os: mac
-
menu$: user.contextual_menu_open()
menu <user.menu_item>: user.menu_item_select(menu_item)
menu hover <user.menu_item>: user.menu_item_hover(menu_item)

status menus$: user.status_menus_toggle()
status <user.status_menu>:
    user.status_menus_hide()
    user.menu_item_select(status_menu)
status hover <user.status_menu>:
    user.status_menus_hide()
    user.menu_item_hover(status_menu)
status touch <user.status_menu>:
    user.status_menus_hide()
    user.menu_item_hover(status_menu)
    mouse_click()
