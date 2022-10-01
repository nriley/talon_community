from talon import actions, ui

DEFAULT_DISABLE_BUNDLE_IDS = frozenset(
    {
        "com.apple.FaceTime",
        "com.bluejeansnet.Blue",
        "com.microsoft.teams",
        "com.webex.meetingmanager",
        "us.zoom.xos",
    }
)

was_enabled_globally = False
disabling_app_bundle_ids = set()


def app_launched(app):
    global was_enabled_globally, disabling_app_bundle_ids
    launched_app_bundle_id = app.bundle
    # print(f'launched {launched_app_bundle_id}')
    # print(f'was_enabled_globally: {was_enabled_globally}')
    # print(f'disabling_app_bundle_ids: {disabling_app_bundle_ids}')
    if launched_app_bundle_id not in DEFAULT_DISABLE_BUNDLE_IDS:
        return
    was_enabled_globally = actions.speech.enabled()
    if was_enabled_globally:
        actions.user.switcher_hide_running()
        actions.user.history_disable()
        actions.user.homophones_hide()
        actions.user.help_hide()
        actions.speech.disable()
        disabling_app_bundle_ids.add(launched_app_bundle_id)


def app_quit(app):
    global was_enabled_globally, disabling_app_bundle_ids
    quit_app_bundle_id = app.bundle
    # print(f'quit {quit_app_bundle_id}')
    # print(f'was_enabled_globally: {was_enabled_globally}')
    # print(f'disabling_app_bundle_ids: {disabling_app_bundle_ids}')
    if quit_app_bundle_id not in disabling_app_bundle_ids:
        return
    disabling_app_bundle_ids.discard(quit_app_bundle_id)
    if was_enabled_globally:
        if len(disabling_app_bundle_ids) == 0:
            # print(f'enabling...')
            actions.speech.enable()


def register_events():
    ui.register("app_launch", app_launched)
    ui.register("app_close", app_quit)


# if we try to do this on module load at startup, the action speech.enabled is not yet defined
from talon import app

app.register("ready", register_events)
