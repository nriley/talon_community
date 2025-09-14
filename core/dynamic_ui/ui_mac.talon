os: mac
-

[gooey] button <user.ui_active_window_button>:
    user.ui_element_click(ui_active_window_button)

button hover <user.ui_active_window_button>:
    user.ui_element_hover(ui_active_window_button)

field <user.ui_active_window_field>: user.ui_element_focus(ui_active_window_field)

field hover <user.ui_active_window_field>:
    user.ui_element_hover(ui_active_window_field)

field menu <user.ui_active_window_field>: user.ui_element_menu(ui_active_window_field)
