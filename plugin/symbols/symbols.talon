question [mark]: "?"
check mark: "✓"
splash: " - "
double dash: "--"
triple quote: "'''"
triple grave | triple back tick | gravy: "```"
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

# Insert delimiter pairs
<user.delimiter_pair>: user.delimiter_pair_insert(delimiter_pair)

# Wrap selection with delimiter pairs
<user.delimiter_pair> that: user.delimiter_pair_wrap_selection(delimiter_pair)
