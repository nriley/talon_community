import types

from talon import Module, actions

mod = Module()


class NotifyException(Exception):
    # reduce exception width when printed
    __module__ = ""


@mod.action_class
class Actions:
    def notify_exception(
        body: str = "", title: str = "", subtitle: str = "", sound: bool = False
    ):
        """Show a desktop notification and raise an exception"""
        actions.app.notify(body, title, subtitle, sound)
        message = ": ".join(m for m in (title, subtitle, body) if m)
        raise NotifyException(message)  # see caller above
