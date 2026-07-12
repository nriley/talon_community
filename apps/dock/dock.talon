os: mac
-

^desktop$: user.dock_send_notification("com.apple.showdesktop.awake")
^app windows$: user.dock_app_expose()
^windows of <user.running_applications>$:
    app = user.get_running_app(running_applications)
    user.dock_app_expose(app)
^launch pad$: user.dock_send_notification("com.apple.launchpad.toggle")
