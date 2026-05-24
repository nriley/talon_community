from talon import Context, Module, actions, app, cron, imgui

mod = Module()
ctx = Context()


CALL_MICROPHONE = "SpeechMike III"
pre_call_microphone = None

EXCLUDE_MICROPHONES = {
    "LG UltraFine Display Audio",
    "Camo Microphone",
    "Microsoft Teams Audio Device",
    "MOTIV Mix Virtual Output",
    "RØDE Connect System",
    "RØDE Connect Virtual",
    "WebexMediaAudioDevice",
    "ZoomAudioDevice",
}

microphone_device_list = []
update_microphone_cron_job = None


def update_microphone_list():
    global microphone_device_list
    # By convention, None and System Default are listed first
    # to match the Talon microphone menu.
    microphone_device_list = ["None", "System Default"]

    devices = [
        device
        for device in actions.sound.microphones()
        if device not in microphone_device_list and device not in EXCLUDE_MICROPHONES
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
    gui.text("Microphone list updates every 5 seconds")
    gui.spacer()
    active_microphone = actions.sound.active_microphone()
    for index, item in enumerate(microphone_device_list, 1):
        if gui.button(
            f"{f'[{index}] ' if index < 10 else ''}{item}{' — active' if item == active_microphone else ''}"
        ):
            actions.user.microphone_select(index)
    gui.spacer()
    if gui.button("[esc] microphone close"):
        actions.user.microphone_selection_hide()


@mod.action_class
class Actions:
    def microphone_selection_toggle():
        """Show GUI for choosing the Talon microphone"""
        global update_microphone_cron_job

        if gui.showing:
            actions.user.microphone_selection_hide()
            return
        update_microphone_list()
        gui.show()
        ctx.tags = ["user.microphone_selection_open"]
        update_microphone_cron_job = cron.interval("5s", update_microphone_list)

    def microphone_selection_hide():
        """Hide the microphone selection GUI"""
        global update_microphone_cron_job

        gui.hide()
        ctx.tags = []
        cron.cancel(update_microphone_cron_job)
        update_microphone_cron_job = None

    def microphone_select(index: int):
        """Selects a microphone"""
        if index >= 1 and index <= len(microphone_device_list):
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
