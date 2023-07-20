from talon import Context, Module, actions, app, cron, ui

FDLINK_APPLICATION = None

if app.platform == "windows":
    import win32com.client
    from pywintypes import com_error

    FDLINK_APPLICATION = win32com.client.Dispatch("FDLink.Application")

mod = Module()
ctx = Context()
ctx.matches = """
os: windows
"""


@mod.action_class
class Actions:
    def fd_is_running() -> bool:
        """Is Fluency Direct running?"""
        return False

    def fd_is_listening() -> bool:
        """Is Fluency Direct listening?"""
        return False

    def disable_fd():
        """Disable Fluency Direct"""

    def enable_fd():
        """Enable Fluency Direct via a keyboard shortcut"""


@Context().action_class("user")
class FallbackUserActions:
    def disable_fd():
        pass

    def enable_fd():
        pass


@ctx.action_class("user")
class UserActions:
    def fd_is_running():
        if FDLINK_APPLICATION is None:
            return False
        return FDLINK_APPLICATION.IsRunning()

    def fd_is_listening():
        return fd_listening()

    def disable_fd():
        if fdrc := fd_recording_control():
            # can't enable from FD UI while recording is disabled
            fdrc.EnableRecording(False)
            # however, recording remains off after reenabled
            fdrc.EnableRecording(True)

    def enable_fd():
        if not actions.user.fd_is_running():
            return
        # start out with FD in a known state
        actions.user.disable_fd()
        actions.key("`")


FD_RECORDING_CONTROL = None

def fd_recording_control():
    global FD_RECORDING_CONTROL

    if not actions.user.fd_is_running():
        FD_RECORDING_CONTROL = None
        return None

    if FD_RECORDING_CONTROL is None:
        fdas = FDLINK_APPLICATION.Connect()
        if fdas is None:
            return None

        FD_RECORDING_CONTROL = fdas.GetRecordingControl()
        if FD_RECORDING_CONTROL is None:
            return None

    return FD_RECORDING_CONTROL

def fd_listening():
    global FD_RECORDING_CONTROL

    if fdrc := fd_recording_control():
        try:
            return fdrc.GetRecognizerStatus() == 1
        except com_error:
            FD_RECORDING_CONTROL = None
    
    return False


def toggle_talon_by_fd_listening():
    if not actions.speech.enabled():
        # SpeechMike does not listen unless I hold it up - can switch back and forth
        # Other microphones currently require I manually reenable Talon with a voice or
        # keyboard command
        if (
            "SpeechMike III" in actions.sound.active_microphone()
            and not fd_listening()
            and not actions.user.speech_suspended()
        ):
            actions.speech.enable()
        return

    if fd_listening():
        print("FD listening - disabling Talon")
        actions.speech.disable()


if FDLINK_APPLICATION:
    app.register("ready", lambda: cron.interval("500ms", toggle_talon_by_fd_listening))
