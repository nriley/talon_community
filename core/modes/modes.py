from talon import Context, Module, actions, app, scope, speech_system, ui

mod = Module()
ctx_sleep = Context()
ctx_awake = Context()

modes = {
    "presentation": "a more strict form of sleep where only a more strict wake up command works",
}

for key, value in modes.items():
    mod.mode(key, value)

ctx_sleep.matches = r"""
mode: sleep
"""

ctx_awake.matches = r"""
not mode: sleep
"""


@ctx_sleep.action_class("speech")
class ActionsSleepMode:
    def disable():
        actions.app.notify("Talon is already asleep")


@ctx_awake.action_class("speech")
class ActionsAwakeMode:
    def enable():
        actions.app.notify("Talon is already awake")


def dictation_mode_active() -> bool:
    return "dictation" in scope.get("mode", ())


@mod.action_class
class Actions:
    def command_mode():
        """Enable command mode"""
        actions.mode.disable("sleep")
        actions.mode.disable("dictation")
        actions.mode.enable("command")

    def dictation_mode():
        """Enable dictation mode"""
        actions.mode.disable("sleep")
        actions.mode.disable("command")
        actions.mode.enable("dictation")
        actions.user.code_clear_language_mode()
        actions.user.gdb_disable()

    def talon_mode():
        """For windows and Mac with Dragon, enables Talon commands and Dragon's command mode."""
        actions.speech.enable()

        engine = speech_system.engine.name
        # app.notify(engine)
        if "dragon" in engine:
            if app.platform == "mac":
                actions.user.dragon_engine_sleep()
            elif app.platform == "windows":
                actions.user.dragon_engine_wake()
                # note: this may not do anything for all versions of Dragon. Requires Pro.
                actions.user.dragon_engine_command_mode()

    def dragon_mode():
        """For windows and Mac with Dragon, disables Talon commands and exits Dragon's command mode"""
        engine = speech_system.engine.name
        # app.notify(engine)

        if "dragon" in engine:
            # app.notify("dragon mode")
            actions.speech.disable()
            if app.platform == "mac":
                actions.user.dragon_engine_wake()
            elif app.platform == "windows":
                actions.user.dragon_engine_wake()
                # note: this may not do anything for all versions of Dragon. Requires Pro.
                actions.user.dragon_engine_normal_mode()

    def dictation_mode():
        """Switch to dictation mode."""
        actions.user.status_add("Dictation Mode")
        actions.mode.disable("sleep")
        actions.mode.enable("command")  # mixed mode
        actions.mode.enable("dictation")
        actions.user.gdb_disable()

    def command_mode():
        """Switch to command mode."""
        actions.user.status_remove("Dictation Mode")
        actions.mode.disable("sleep")
        actions.mode.disable("dictation")
        actions.mode.enable("command")

    def toggle_dictation_mode():
        """Switch from dictation to command mode or vice versa."""
        if dictation_mode_active():
            actions.user.command_mode()
        else:
            actions.user.dictation_mode()

    def is_active_mode() -> bool:
        """Returns whether we are in command and/or dictation mode, and not sleep mode"""
        modes = scope.get("mode", ())
        return "sleep" not in modes and ("dictation" in modes or "command" in modes)

    def enter_user_mode(mode: str):
        """Save current modes, disable dictation/command and enable user.<mode> mode if inactive"""
        if ("user." + mode) in scope.get("mode", ()):
            return
        actions.mode.save()
        actions.mode.disable("dictation")
        actions.mode.disable("command")
        actions.mode.enable("user." + mode)

    def exit_user_mode(mode: str):
        """Disable user.<mode> mode if active, restoring prior modes"""
        if ("user." + mode) not in scope.get("mode", ()):
            return
        actions.mode.restore()


dictation_apps = set()


def set_command_mode_on_app_deactivate(app):
    global dictation_apps

    if not actions.user.is_active_mode():
        return

    if dictation_mode_active():
        dictation_apps.add(app)
        actions.user.command_mode()
    elif app in dictation_apps:
        dictation_apps.remove(app)


def restore_dictation_mode_on_app_activate(app):
    if not actions.user.is_active_mode():
        return

    if app in dictation_apps and not dictation_mode_active():
        actions.user.dictation_mode()


def remove_dictation_app_on_quit(app):
    global dictation_apps

    if app in dictation_apps:
        dictation_apps.remove(app)


def on_ready():
    ui.register("app_deactivate", set_command_mode_on_app_deactivate)
    ui.register("app_activate", restore_dictation_mode_on_app_activate)
    ui.register("app_close", remove_dictation_app_on_quit)


app.register("ready", on_ready)
