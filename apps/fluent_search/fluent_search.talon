os: windows
-
# Fluent Search provides equivalents to my common uses of
# LaunchBar, Contexts, Vimac and menu search on Mac.

# If you have different keyboard shortcuts configured, you will need
# to replace them here.

# -- Vimac
# Search in-app using Screen hotkey
^nav$: key(alt-;)

# Search using Screen hotkey on (single) screen
^nav screen$: key(ctrl-alt-;)

# -- LaunchBar
# Search hotkey (in fluent_search.py)
launch <user.text>: user.fluent_search("apps\t{text}")
launch brief {user.abbreviation}: user.fluent_search("apps\t{abbreviation}")
launch bar: user.fluent_search("")

# Search using Processes hotkey
launch running: key(ctrl-alt-shift-space)

# -- Contexts
^con [<user.text>]: user.fluent_search(text or "")

# -- Menu search
# In-app search hotkey
^menu [<user.text>]$:
    key(alt-shift-/)
    user.paste(text or "")
