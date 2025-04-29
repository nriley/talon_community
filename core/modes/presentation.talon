mode: user.presentation
-
^stop presenting$:
    mode.disable("user.presentation")
    mode.restore()

<phrase>: skip()
