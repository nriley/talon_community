os: mac
-
menu$: user.contextual_menu_open()
menu <user.menu_item>: user.menu_item_select(menu_item)
menu hover <user.menu_item>: user.menu_item_hover(menu_item)

extra <user.menu_extra>: user.menu_item_select(menu_extra)
extra hover <user.menu_extra>: user.menu_item_hover(menu_extra)
extra touch <user.menu_extra>:
    user.menu_item_hover(menu_extra)
    mouse_click()
