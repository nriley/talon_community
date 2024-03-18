from talon import Context, Module, actions, app, imgui
from talon.lib import cubeb

mod = Module()
ctx = Context()

cubeb_ctx = cubeb.Context()

CALL_MICROPHONE = "SpeechMike III"
pre_call_microphone = None

EXCLUDE_MICROPHONES = {
    "LG UltraFine Display Audio",
    "Camo Microphone",
    "Microsoft Teams Audio Device",
    "RØDE Connect System",
    "RØDE Connect Virtual",
    "WebexMediaAudioDevice",
    "ZoomAudioDevice",
}

microphone_device_list = []


# by convention, None and System Default are listed first
# to match the Talon context menu.
def update_microphone_list():
    global microphone_device_list
    microphone_device_list = ["None", "System Default"]

    # On Windows, it's presently necessary to check the state, or
    # we will get any and every microphone that was ever connected.
    devices = [
        dev.name
        for dev in cubeb_ctx.inputs()
        if dev.state == cubeb.DeviceState.ENABLED
        and dev.name not in EXCLUDE_MICROPHONES
    ]

    devices.sort()
    microphone_device_list += devices


def devices_changed(device_type):
    update_microphone_list()


mod.tag(
    "microphone_selection_open",
    "tag for commands that are available only when the list of microphones is visible",
)


@imgui.open()
def gui(gui: imgui.GUI):
    gui.text("Click or type to select a microphone")
    gui.text("(or say “microphone pick #”)")
    gui.line()
    active_microphone = actions.sound.active_microphone()
    for index, item in enumerate(microphone_device_list, 1):
        if gui.button(
            f"{f'[{index}] ' if index < 10 else ''}{item}{' — active' if item == active_microphone else ''}"
        ):
            actions.user.microphone_select(index)

    gui.spacer()
    if gui.button("[esc] Microphone close"):
        actions.user.microphone_selection_hide()


@mod.action_class
class Actions:
    def microphone_selection_toggle():
        """Show GUI for choosing the Talon microphone"""
        if gui.showing:
            actions.user.microphone_selection_hide()
            return
        update_microphone_list()
        gui.show()
        ctx.tags = ["user.microphone_selection_open"]

    def microphone_selection_hide():
        """Hide the microphone selection GUI"""
        gui.hide()
        ctx.tags = []

    def microphone_select(index: int):
        """Selects a microphone"""
        if 1 <= index and index <= len(microphone_device_list):
            actions.sound.set_microphone(microphone_device_list[index - 1])
            actions.user.microphone_selection_hide()

    def microphone_switch() -> bool:
        """Switches to a secondary microphone for use during a call (returning success)"""
        global CALL_MICROPHONE, pre_call_microphone
        microphones = actions.sound.microphones()
        for microphone in microphones:
            if CALL_MICROPHONE in microphone:
                current_microphone = actions.sound.active_microphone()
                if microphone == current_microphone:
                    return False  # same microphone
                pre_call_microphone = current_microphone
                actions.sound.set_microphone(microphone)
                app.notify(title="Switched microphone during call", body=microphone)
                return True
        return False

    def microphone_restore():
        """Restores the primary microphone after a call"""
        if not pre_call_microphone:
            app.notify(
                title="No prior microphone to restore",
                subtitle="Current microphone:",
                body=actions.sound.active_microphone(),
            )
        else:
            actions.sound.set_microphone(pre_call_microphone)
            app.notify(title="Restored prior microphone", body=pre_call_microphone)

    def talon_drop_in_progress_audio():
        """Uses a hack to tell Talon to drop all in progress audio"""
        # https://github.com/talonvoice/talon/issues/538
        active_microphone = actions.sound.active_microphone()
        actions.sound.set_microphone("None")
        actions.sound.set_microphone(active_microphone)


def on_ready():
    cubeb_ctx.register("devices_changed", devices_changed)
    update_microphone_list()


app.register("ready", on_ready)
