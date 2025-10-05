os: mac
-

[gooey] button <user.ui_active_window_button>:
    user.ui_element_click(ui_active_window_button)
button hover <user.ui_active_window_button>:
    user.ui_element_hover(ui_active_window_button)
button menu <user.ui_active_window_button>:
    user.ui_element_menu(ui_active_window_button)
help buttons: user.help_list("user.ui_active_window_button")

[gooey] field <user.ui_active_window_field>:
    user.ui_element_focus(ui_active_window_field)
field hover <user.ui_active_window_field>:
    user.ui_element_hover(ui_active_window_field)
field menu <user.ui_active_window_field>: user.ui_element_menu(ui_active_window_field)
help fields: user.help_list("user.ui_active_window_field")

[gooey] list <user.ui_active_window_list>: user.ui_element_focus(ui_active_window_list)
list menu <user.ui_active_window_list>: user.ui_element_menu(ui_active_window_list)
list hover <user.ui_active_window_list>: user.ui_element_hover(ui_active_window_list)
help lists: user.help_list("user.ui_active_window_list")

[gooey] row <user.ui_focused_list_visible_row>:
    user.ui_element_select(ui_focused_list_visible_row)
row menu <user.ui_focused_list_visible_row>:
    user.ui_element_menu(ui_focused_list_visible_row)
row hover <user.ui_focused_list_visible_row>:
    user.ui_element_hover(ui_focused_list_visible_row)
help rows: user.help_list("user.ui_focused_list_visible_row")

[gooey] row all <user.ui_focused_list_row>: user.ui_element_select(ui_focused_list_row)
row all menu <user.ui_focused_list_row>: user.ui_element_menu(ui_focused_list_row)
row all hover <user.ui_focused_list_row>: user.ui_element_hover(ui_focused_list_row)
help rows all: user.help_list("user.ui_focused_list_row")

[gooey] sidebar <user.ui_sidebar_row>: user.ui_element_select(ui_sidebar_row)
sidebar menu <user.ui_sidebar_row>: user.ui_element_menu(ui_sidebar_row)
sidebar hover <user.ui_sidebar_row>: user.ui_element_hover(ui_sidebar_row)
help sidebar: user.help_list("user.ui_sidebar_row")
