question [mark]: "?"
check mark: "✓"
splash: " - "
double dash: "--"
triple quote: "'''"
(triple grave | triple back tick | gravy): insert("```")
(dot dot | dotdot): ".."
ellipsis: "…"
comgap: ", "
colgap: ": "
semgap: "; "
stop: ". "
point: "."
possessive: "’s"
plus: "+"
arrow: "->"
dub arrow: "=>"
left arrow: user.paste("←")
right arrow: user.paste("→")
up arrow: user.paste("↑")
down arrow: user.paste("↓")
right arrowhead: user.paste("▸")
shift key: user.paste("⇧")
command key: user.paste("⌘")
control key: user.paste("⌃")
option key: user.paste("⌥")
empty dub string: user.insert_between('"', '"')
empty escaped (dub string | dub quotes): user.insert_between('\\"', '\\"')
empty string: user.insert_between("'", "'")
empty escaped string: user.insert_between("\\'", "\\'")
inside angle brackets: user.insert_between("<", ">")
(inside parens | args): user.insert_between("(", ")")
inside (brackets | square brackets | list): user.insert_between("[", "]")
inside (braces | curly brackets): user.insert_between("{", "}")
inside percent: user.insert_between("%", "%")
inside (quotes | string): user.insert_between("'", "'")
inside dub quotes: user.insert_between('"', '"')
inside back ticks: user.insert_between("`", "`")
angle that:
    text = edit.selected_text()
    user.paste("<{text}>")
(bracket | square bracket) that:
    text = edit.selected_text()
    user.paste("[{text}]")
(brace | curly bracket) that:
    text = edit.selected_text()
    user.paste("{{{text}}}")
(parens | args) that:
    text = edit.selected_text()
    user.paste("({text})")
percent that:
    text = edit.selected_text()
    user.paste("%{text}%")
quote that:
    text = edit.selected_text()
    user.paste("'{text}'")
(double quote | dub quote) that:
    text = edit.selected_text()
    user.paste('"{text}"')
back tick that:
    text = edit.selected_text()
    user.paste("`{text}`")
