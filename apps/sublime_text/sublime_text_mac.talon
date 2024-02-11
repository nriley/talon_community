os: mac
app.bundle: com.sublimetext.4
-
tag(): user.file_manager
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
# tag(): user.snippets
tag(): user.tabs

# NOTE: for Talon's context-sensitive dictation to work properly in Sublime Text,
# you need to set "copy_with_empty_selection": false in your settings.

bar switch: key(cmd-k cmd-b)

file hunt [<user.text>]:
    key(cmd-p)
    insert(text or "")

symbol hunt [<user.text>]:
    key(cmd-shift-r)
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

definition show: key(cmd-alt-down)

slap: key(cmd-enter)

# navigate through multifile search (match) results
(match | result) next: key(f4 cmd-g)
(match | result) previous: key(shift-f4 cmd-g)

# history navigation
go back: key(ctrl--)
go forward: key(ctrl-shift--)

# talonfmt barfs if the parentheses below are missing:
# https://github.com/wenkokke/talonfmt/issues/93
^(repository | repo)$:
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
