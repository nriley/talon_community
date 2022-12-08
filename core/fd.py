from talon import Context, Module, actions, app, cron, ui
from talon.experimental.locate import locate_in_image

fda = None

if app.platform == "windows":
    import win32api
    import win32com.client

    # needed? On Win10, this is in C:\ProgramData\MModal\DesktopDictationClient\Versions\[...]
    win32api.SetDllDirectory(r"C:\MModal\Server")
    fda = win32com.client.Dispatch("FDLink.Application")

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
        """Enable Fluency Direct via a keyboard shortcut."""


@Context().action_class("user")
class FallbackUserActions:
    def disable_fd():
        pass

    def enable_fd():
        pass


@ctx.action_class("user")
class UserActions:
    def fd_is_running():
        if fda is None:
            return False
        return fda.IsRunning()

    def fd_is_listening():
        return fd_listening()
    
    def disable_fd():
        if fda is None:
            return

        if not actions.user.fd_is_running():
            return

        fdas = fda.Connect()
        if fdas is None:
            return  # unable to connect

        # this just turns on/off dictation; leaves commands enabled
        # fddc = fdas.GetDictationControl()
        # fddc.SetEnabled(True)

        # can't enable from FD UI while recording is disabled
        fdrc = fdas.GetRecordingControl()
        fdrc.EnableRecording(False)
        # however, recording remains off after reenabled
        fdrc.EnableRecording(True)

    def enable_fd():
        if not actions.user.fd_is_running():
            return
        # start out with FD in a known state
        actions.user.disable_fd()
        actions.key("`")


def fd_window():
    fd_app = ui.apps(name="M*Modal Fluency Direct")
    if not fd_app:
        return None
    fd_app = fd_app[0]
    try:
        return next(
            window
            for window in fd_app.windows()
            if window.title == "M*Modal Fluency Direct"
        )
    except StopIteration:
        return None


def fd_listening():
    window = fd_window()
    if not window:
        return False

    return actions.user.mouse_helper_find_template_relative(
        "fd_listening.png", region=window.rect
    )


def disable_talon_if_fd_listening():
    if not actions.speech.enabled():
        return

    if fd_listening():
        print("FD listening - disabling Talon")
        actions.speech.disable()


if app.platform == "windows":
    app.register("ready", lambda: cron.interval("2s", disable_talon_if_fd_listening))
