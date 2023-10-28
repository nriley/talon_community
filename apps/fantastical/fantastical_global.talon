os: mac
-
^fantastical [<user.text>]:
    user.fantastical_parse(user.formatted_text("{text or ''}", "CAPITALIZE_FIRST_WORD"))

^fantastical <user.text> over:
    user.fantastical_parse("{user.formatted_text(user.text, 'CAPITALIZE_FIRST_WORD')} ")
    sleep(500ms)

^calendar mini: user.fantastical_show_mini_calendar()

^calendar open: user.fantastical_show_calendar()

^calendar join:
    user.fantastical_show_menu()
    key(down)
