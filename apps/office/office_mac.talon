app: office_mac
-
document: user.office_document_actions()

ribbon <user.ribbon_item>: user.office_mac_ribbon_item_select(ribbon_item)
ribbon hover <user.ribbon_item>: user.office_mac_ribbon_item_hover(ribbon_item)

help ribbon: user.help_list("user.ribbon_items")
