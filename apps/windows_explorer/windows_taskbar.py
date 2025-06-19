import os

from talon import Context, Module, actions, app, ui

mod = Module()

ctx = Context()
ctx.matches = """
os: windows
"""


@mod.action_class
class Actions:
    def click_system_tray_button(button_names: str):
        """Click the system tray button with one of the |-separated names"""

@ctx.action_class("user")
class UserActions:
    def click_system_tray_button(button_names: str):
        explorer = ui.apps(name="Windows Explorer")[0]
        try:
            taskbar = next(
                window for window in explorer.windows() if window.cls == "Shell_TrayWnd"
            )
        except StopIteration:
            print("Unable to find system tray window - instead found:")
            for w in explorer.windows():
                print(f"\t- {w.cls=}; {w.title=}")
            return
        pane = taskbar.element.find_one(class_name="Windows.UI.Input.InputSite.WindowClass", max_depth=0)
        try:
            actions.user.mouse_helper_position_save()
            buttons = pane.find(class_name="SystemTray.NormalButton", max_depth=0)
            next(
                button for button in buttons if button.name in button_names.split("|")
            ).invoke_pattern.invoke()
            actions.user.mouse_helper_position_restore()
        except StopIteration:
            print("No matching system tray button found - names found:")
            for e in buttons:
                print(f"\t- {e.name}")
