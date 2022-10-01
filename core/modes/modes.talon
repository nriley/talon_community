not mode: sleep
-
^dictation mode$: user.dictation_mode()

^command mode$: user.command_mode()

key(ctrl-alt-`): user.toggle_dictation_mode()
