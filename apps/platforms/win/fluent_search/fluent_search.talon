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
# Search hotkey
launch <user.text>:
	key(ctrl-alt-space backspace)
	user.paste(text)

launch brief {user.abbreviation}:
	key(ctrl-alt-space backspace)
	user.paste(abbreviation)

launch bar:
	key(ctrl-alt-space)

# Search using Processes hotkey
launch running:
	key(ctrl-alt-shift-space)

# -- Contexts
^con [<user.text>]:
	key(ctrl-alt-space)
	user.paste(text or "")

# -- Menu search
# In-app search hotkey
^menu [<user.text>]$:
	key(alt-shift-/)
	user.paste(text or "")
