os: mac
-

# XXX "watch" is a conformer workaround

(launch | watch) <user.text>: user.launchbar_select(text)

(launch | watch) brief {user.abbreviation}: user.launchbar_select(abbreviation)

(launch | watch) bar: user.launch_or_focus_bundle("at.obdev.LaunchBar")

(launch | watch) running: user.launchbar_action("Running Applications", "")

web search <phrase>: user.launchbar_action("Google", "{phrase}")

# If you have different keyboard shortcuts configured, you will need
# to replace them here.  Mine are:

# Instant Send: Double Control (which I have mapped to caps lock)
# Show clipboard history: Control-Option-Command-V

(launch | watch) paste: key(ctrl-cmd-alt-v)

(launch | watch) send:
    key(ctrl:down)
    sleep(10ms)
    key(ctrl:up ctrl:down)
    sleep(10ms)
    key(ctrl:up)
