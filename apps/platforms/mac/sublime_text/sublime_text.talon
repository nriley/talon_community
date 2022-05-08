os: mac
app.bundle: com.sublimetext.4
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
# tag(): user.snippets
tag(): user.tabs

# NOTE: for Talon's context-sensitive dictation to work properly in Sublime Text,
# you need to set "copy_with_empty_selection": false in your settings.

toggle sidebar: key(cmd-k cmd-b)

file hunt [<user.text>]:
    key(cmd-p)
    insert(text or "")

please [<user.text>]:
    key(cmd-shift-p)
    insert(text or "")

project switch [<user.text>]:
    key(cmd-ctrl-p)
    insert(text or "")

project symbol [<user.text>]:
    key(cmd-shift-r)
    insert(text or "")

complete: key(ctrl-space)
[un]comment that: code.toggle_comment()

slap: key(cmd-enter)

# navigate through multifile search results
result next: key(f4 cmd-g)
result previous: key(shift-f4 cmd-g)

# history navigation
go back: key(ctrl--)
go forward: key(ctrl-shift--)

^repository | repo$:
    key(cmd-shift-p)
    insert("Sublime Merge: Open Repository")
    key(enter)

# Search through Talon or Python files when editing Talon configuration
hunt pie [<user.text>]$:
    text = text or ""
    user.sublime_text_find_in_project_files(text, "*.py,*.pyi")

hunt talon [<user.text>]$:
    text = text or ""
    user.sublime_text_find_in_project_files(text, "*.talon")
