from dataclasses import dataclass, field
from threading import get_ident

from talon import Context, Module, actions, app, imgui, ui

ctx = Context()
mod = Module()
mod.tag("help_focused_open", "tag for showing the focused help GUI")


def text_attrs(gui, obj, attrs):
    for attr in attrs:
        try:
            val = getattr(obj, attr, None)
        except Exception as e:
            val = "raised " + repr(e)
        if val:
            gui.text(f"{attr}: {val}")


def title(gui, title, spacer=True):
    if spacer:
        gui.spacer()
    gui.text(title)
    gui.line()


def hide_button(gui):
    gui.spacer()
    if gui.button("focused hide"):
        actions.user.help_focused_toggle()


@dataclass
class ImguiRecording:
    gui: imgui.GUI = None
    recording: list[tuple] = field(default_factory=list)
    invalid: bool = False

    def __getattr__(self, attr):
        def f(*args):
            self.recording.append((attr, args))
            getattr(self.gui, attr)(*args)

        return f

    def playback(self, gui):
        recording = self.recording
        if len(recording) == 0:
            return False

        for m, args in recording:
            getattr(gui, m)(*args)

        return True

    def stop(self):
        self.gui = None
        if self.invalid:
            self.recording = []
            self.invalid = False

    def clear(self, *args):
        self.invalid = True
        if self.gui is None:
            self.recording = []


FOCUSED_HELP = None


@imgui.open(x=ui.main_screen().x)
def focused_help(gui: imgui.GUI):
    global FOCUSED_HELP
    if FOCUSED_HELP.playback(gui):
        hide_button(gui)
        return
    else:
        FOCUSED_HELP.gui = gui
    gui = FOCUSED_HELP

    title(gui, f"Focused", spacer=False)

    match app.platform:
        case "mac":
            pass
        case _:
            gui.text("Not currently supported on Windows or Linux")
            hide_button(gui)
            return

    try:
        focused_element = ui.focused_element()
    except RuntimeError:
        focused_element = None
    if focused_element:
        title(gui, "Element")
        text_attrs(
            gui,
            focused_element,
            (
                "AXRole",
                "AXSubrole",
                "parent",
                "window",
            ),
        )

    if active_window := ui.active_window():
        title(gui, "Window")
        text_attrs(gui, active_window, ("title", "rect", "id", "app"))

    if active_menu := ui.active_menu():
        title(gui, "Menu")
        if not active_menu.attrs:
            gui.text(repr(active_menu))
        else:
            text_attrs(
                gui,
                active_menu,
                (
                    "AXRole",
                    "parent",
                    "window",
                ),
            )
    hide_button(gui.gui)
    gui.stop()


@mod.action_class
class Actions:
    def help_focused_toggle():
        """Toggle focused help GUI"""
        global FOCUSED_HELP

        if focused_help.showing:
            ctx.tags = []
            focused_help.hide()
            ui.unregister("", FOCUSED_HELP.clear)
            FOCUSED_HELP = None
        else:
            ctx.tags = ["user.help_focused_open"]
            FOCUSED_HELP = ImguiRecording()
            focused_help.show()
            ui.register("", FOCUSED_HELP.clear)
