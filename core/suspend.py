from talon import Context, Module, actions, ui

DEFAULT_DISABLE_BUNDLE_IDS = frozenset(
    {
        "com.apple.FaceTime",
        "com.bluejeansnet.Blue",
        "com.hnc.Discord",
    }
)

was_enabled_globally = False
disabling_app_bundle_ids = set()

mod = Module()
ctx = Context()


@ctx.action_class("user")
class UserActions:
    def meeting_started(app, window):
        suspend_by_app(window.app)
        actions.next(app, window)

    def meeting_ended(app, window):
        resume_if_suspended_by_app(window.app)
        actions.next(app, window)


@mod.action_class
class Actions:
    def speech_suspended() -> bool:
        """Returns whether speech recognition is suspended due to an in-progress call"""
        for bundle_id in disabling_app_bundle_ids:
            if ui.apps(bundle=bundle_id):
                return True
        return False


def suspend_by_app(app):
    global was_enabled_globally, disabling_app_bundle_ids

    if app.bundle in disabling_app_bundle_ids:
        return

    was_enabled_globally = actions.speech.enabled()
    if was_enabled_globally:
        if not actions.user.microphone_switch():
            actions.user.switcher_hide_running()
            actions.user.history_disable()
            actions.user.homophones_hide()
            actions.user.help_hide()
            actions.speech.disable()
        disabling_app_bundle_ids.add(app.bundle)


def app_launched(app):
    if not (launched_app_bundle_id := app.bundle):
        return
    # print(f"+ launched {launched_app_bundle_id}; {was_enabled_globally=}")
    # print(f"disabling_app_bundle_ids: {disabling_app_bundle_ids}")
    if launched_app_bundle_id not in DEFAULT_DISABLE_BUNDLE_IDS:
        return

    suspend_by_app(app)


def resume_if_suspended_by_app(app):
    global was_enabled_globally, disabling_app_bundle_ids
    if not (app_bundle_id := app.bundle):
        return
    # print(f"- left meeting in {app_bundle_id}; {was_enabled_globally=}")
    # print(f"disabling_app_bundle_ids: {disabling_app_bundle_ids}")
    if app_bundle_id not in disabling_app_bundle_ids:
        return
    disabling_app_bundle_ids.discard(app_bundle_id)
    if was_enabled_globally:
        if len(disabling_app_bundle_ids) == 0:
            # print(f'enabling...')
            actions.speech.enable()
            actions.user.microphone_restore()


def register_events():
    ui.register("app_launch", app_launched)
    ui.register("app_close", resume_if_suspended_by_app)


# if we try to do this on module load at startup, the action speech.enabled is not yet defined
from talon import app

app.register("ready", register_events)
