from talon import Context, Module, actions, clip, ui

from .dock_spi import ffi

ctx = Context()
mod = Module()

ctx.matches = """
os: mac
"""


@mod.action_class
class Actions:
    def dock_send_notification(notification: str):
        """Send a CoreDock notification to the macOS Dock using SPI"""


cf = None
appservices = None


def load():
    global cf, appservices
    if cf is not None:
        return

    cf = ffi.dlopen(
        "/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation"
    )
    appservices = ffi.dlopen(
        "/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices"
    )


@ctx.action_class("user")
class UserActions:
    def dock_send_notification(notification: str):
        load()
        notification_cfstr = cf.CFStringCreateWithCString(
            ffi.NULL, notification.encode("utf8"), cf.kCFStringEncodingUTF8
        )
        appservices.CoreDockSendNotification(notification_cfstr, ffi.NULL)
        cf.CFRelease(notification_cfstr)
