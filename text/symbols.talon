question: "?"
check mark: "✓"
dash: "-"
splash: " - "
double dash: "--"
triple quote: "'''"
(triple grave | triple back tick | gravy):
    insert("```")
(dot dot | dotdot): ".."
ellipsis: "…"
em dash: "—"
(en | end) dash: "–"
comgap: ", "
colgap: ": "
semgap: "; "
stop: ". "
point: "."
possessive: "’s"
plus: "+"
arrow: "->"
dub arrow: "=>"
new line: "\\n"
carriage return: "\\r"
line feed: "\\r\\n"
empty dubstring:
    '""'
    key(left)
empty escaped (dubstring|dub quotes):
    '\\"\\"'
    key(left)
    key(left)
empty string:
    "''"
    key(left)
empty escaped string:
    "\\'\\'"
    key(left)
    key(left)
inside angle brackets:
    insert("<>")
    key(left)
(inside parens | args):
    insert("()")
    key(left)
inside (list | brackets):
    insert("[]")
    key(left)
inside braces:
    insert("{}")
    key(left)
inside percent:
    insert("%%")
    key(left)
inside quotes:
    insert('""')
    key(left)
inside back ticks:
    insert("``")
    key(left)
angle that:
    text = edit.selected_text()
    user.paste("<{text}>")
brace that:
    text = edit.selected_text()
    user.paste("{{{text}}}")
bracket that:
    text = edit.selected_text()
    user.paste("[{text}]")
(parens | args) that:
    text = edit.selected_text()
    user.paste("({text})")
percent that:
    text = edit.selected_text()
    user.paste("%{text}%")
quote that:
    text = edit.selected_text()
    user.paste("'{text}'")
(double quote | dubquote) that:
    text = edit.selected_text()
    user.paste('"{text}"')
back tick that:
    text = edit.selected_text()
    user.paste('`{text}`')
