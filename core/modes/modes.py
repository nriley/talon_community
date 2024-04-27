from talon import Context, Module, actions, app, canvas, scope, speech_system, ui
from talon.types import Rect

mod = Module()
ctx_sleep = Context()
ctx_awake = Context()

modes = {
    "admin": "enable extra administration commands terminal (docker, etc)",
    "debug": "a way to force debugger commands to be loaded",
    "ida": "a way to force ida commands to be loaded",
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
    def talon_mode():
        """For windows and Mac with Dragon, enables Talon commands and Dragon's command mode."""
        actions.speech.enable()

        engine = speech_system.engine.name
        # app.notify(engine)
        if "dragon" in engine:
            if app.platform == "mac":
                actions.user.engine_sleep()
            elif app.platform == "windows":
                actions.user.engine_wake()
                # note: this may not do anything for all versions of Dragon. Requires Pro.
                actions.user.engine_mimic("switch to command mode")

    def dragon_mode():
        """For windows and Mac with Dragon, disables Talon commands and exits Dragon's command mode"""
        engine = speech_system.engine.name
        # app.notify(engine)

        if "dragon" in engine:
            # app.notify("dragon mode")
            actions.speech.disable()
            if app.platform == "mac":
                actions.user.engine_wake()
            elif app.platform == "windows":
                actions.user.engine_wake()
                # note: this may not do anything for all versions of Dragon. Requires Pro.
                actions.user.engine_mimic("start normal mode")

    def dictation_mode():
        """Switch to dictation mode."""
        show_mode()
        actions.mode.disable("sleep")
        actions.mode.enable("command")  # mixed mode
        actions.mode.enable("dictation")
        actions.user.code_clear_language_mode()
        actions.user.gdb_disable()

    def command_mode():
        """Switch to command mode."""
        hide_mode()
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


ui.register("app_deactivate", set_command_mode_on_app_deactivate)


def restore_dictation_mode_on_app_activate(app):
    if not actions.user.is_active_mode():
        return

    if app in dictation_apps and not dictation_mode_active():
        actions.user.dictation_mode()


ui.register("app_activate", restore_dictation_mode_on_app_activate)


def remove_dictation_app_on_quit(app):
    global dictation_apps

    if app in dictation_apps:
        dictation_apps.remove(app)


ui.register("app_close", remove_dictation_app_on_quit)

# XXX switch to canvas.overlay instead?

mode_canvases = []


def show_mode():
    global mode_canvases

    if mode_canvases:
        for mode_canvas in mode_canvases:
            mode_canvas.freeze()
        return

    for screen in ui.screens():
        mode_canvas = canvas.Canvas.from_screen(screen)
        mode_canvas.register("draw", draw_mode)
        mode_canvas.freeze()
        mode_canvases.append(mode_canvas)


def hide_mode():
    global mode_canvases

    if not mode_canvases:
        return

    for mode_canvas in mode_canvases:
        mode_canvas.hide()


def draw_mode(canvas):
    paint = canvas.paint
    paint.textsize = 12
    text = "Dictation Mode"
    _, text_rect = paint.measure_text(text)

    try:
        screen = ui.screen_containing(canvas.x, canvas.y)
    except ValueError:  # screen not found?
        return

    screen_rect = screen.visible_rect
    padding_x = 4
    padding_y = 4

    if app.platform == "mac":
        top_left = screen_rect.right - text_rect.width - (padding_x * 2) + 1
        text_offset = 1
    else:
        top_left = screen_rect.left - 1
        text_offset = 0

    bg_rect = Rect(
        top_left,
        screen_rect.y - 1,
        text_rect.width + (padding_x * 2),
        text_rect.height + (padding_y * 2),
    )

    paint.color = "ff0000ff"  # red
    canvas.draw_rect(bg_rect)
    paint.color = "ffffffff"  # white
    canvas.draw_text(
        text,
        bg_rect.x + padding_x + text_offset,
        bg_rect.y + padding_y + text_rect.height - text_offset,
    )


def on_screen_change(screens):
    global mode_canvases

    if not mode_canvases:
        return

    for mode_canvas in mode_canvases:
        mode_canvas.unregister("draw", draw_mode)
        mode_canvas.close()

    mode_canvases = []

    if dictation_mode_active():
        show_mode()


ui.register("screen_change", on_screen_change)
