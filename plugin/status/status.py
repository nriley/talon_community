from talon import Module, app, canvas, ui
from talon.types import Rect

mod = Module()
status_canvases = []
status = set()

# XXX switch to canvas.overlay instead?


@mod.action_class
class Actions:
    def status_add(message: str):
        """Add a status message."""
        global status

        status.add(message)
        show_status()

    def status_remove(message: str):
        """Remove the specified status message."""
        global status

        try:
            status.remove(message)
        except KeyError:
            pass

        if len(status) == 0:
            hide_status()


def show_status():
    global status_canvases

    if status_canvases:
        for status_canvas in status_canvases:
            status_canvas.freeze()
        return

    for screen in ui.screens():
        status_canvas = canvas.Canvas.from_screen(screen)
        status_canvas.register("draw", draw_status)
        status_canvas.freeze()
        status_canvases.append(status_canvas)


def hide_status():
    global status_canvases

    if not status_canvases:
        return

    for mode_canvas in status_canvases:
        mode_canvas.hide()


def draw_status(canvas):
    paint = canvas.paint
    paint.textsize = 12
    text = " | ".join(status)
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
    global status_canvases

    if not status_canvases:
        return

    for status_canvas in status_canvases:
        status_canvas.unregister("draw", draw_status)
        status_canvas.close()

    status_canvases = []

    if len(status) > 0:
        show_status()


def on_ready():
    ui.register("screen_change", on_screen_change)


app.register("ready", on_ready)
