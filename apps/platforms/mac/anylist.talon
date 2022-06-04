os: mac
and app.bundle: com.purplecover.anylist.mac
-

# https://help.anylist.com/articles/desktop-keyboard-shortcuts/

add [<user.text>]:
	key(esc a)
	text = text or ""
	"{user.formatted_text(text, 'CAPITALIZE_FIRST_WORD')}"

done: "x"
edit: "e"
favorite: "f"
save: key(cmd-enter)
