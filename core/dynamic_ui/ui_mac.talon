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

[gooey] (row | item) <user.ui_focused_list_visible_row>:
    user.ui_element_select(ui_focused_list_visible_row)
(row | item) menu <user.ui_focused_list_visible_row>:
    user.ui_element_menu(ui_focused_list_visible_row)
(row | item) hover <user.ui_focused_list_visible_row>:
    user.ui_element_hover(ui_focused_list_visible_row)
row {user.disclosure_action} <user.ui_focused_list_visible_row>:
    user.ui_element_disclose(ui_focused_list_visible_row, disclosure_action)
help (rows | items): user.help_list("user.ui_focused_list_visible_row")

[gooey] (row | item) all <user.ui_focused_list_row>: user.ui_element_select(ui_focused_list_row)
(row | item) all menu <user.ui_focused_list_row>: user.ui_element_menu(ui_focused_list_row)
(row | item) all hover <user.ui_focused_list_row>: user.ui_element_hover(ui_focused_list_row)
help (rows | items) all: user.help_list("user.ui_focused_list_row")

[gooey] sidebar <user.ui_sidebar_row>: user.ui_element_select(ui_sidebar_row)
sidebar menu <user.ui_sidebar_row>: user.ui_element_menu(ui_sidebar_row)
sidebar hover <user.ui_sidebar_row>: user.ui_element_hover(ui_sidebar_row)
sidebar [scroll] {user.scroll_direction}:
    sidebar = user.ui_element_sidebar()
    if sidebar: user.ui_element_scroll(scroll_direction, sidebar)

help sidebar: user.help_list("user.ui_sidebar_row")

head end: user.ui_element_end()
tail end: user.ui_element_end(true)
select head end: user.ui_element_end(false, true)
select tail end: user.ui_element_end(true, true)

scroll {user.scroll_direction}: user.ui_element_scroll(scroll_direction)
