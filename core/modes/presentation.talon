mode: user.presentation
-
tag(): user.pages

^next slide$: user.page_next()
^previous slide$: user.page_previous()
^exit slide show$: key(esc)

^stop presenting$: user.exit_user_mode("presentation")

<phrase>: skip()
