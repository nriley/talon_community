import os

from talon import Context, Module, actions, app, ui

mod = Module()

ctx = Context()
ctx.matches = """
os: windows
"""

@mod.action_class
class Actions:
    def click_taskbar_button(button_names: str):
        """Click the taskbar button with one of the |-separated names"""

def first_matching_child(element, **kw):
    if len(kw) > 1:
        raise Exception("Only one matching attribute supported")
    attr, values = list(kw.items())[0]
    return next(
        e for e in element.children
        if getattr(e, attr) in values
    )

@ctx.action_class("user")
class UserActions:
    def click_taskbar_button(button_names: str):
        explorer = ui.apps(name="Windows Explorer")[0]
        taskbar = next(
            window for window in explorer.windows()
            if window.cls == "Shell_TrayWnd"
        )
        tray = first_matching_child(taskbar.element, class_name=["TrayNotifyWnd"])
        pager = first_matching_child(tray, class_name=["SysPager"])
        toolbar = first_matching_child(pager, class_name=["ToolbarWindow32"])
        try:
            actions.user.mouse_helper_position_save()
            first_matching_child(toolbar, name=button_names.split("|")).invoke_pattern.invoke()
            actions.user.mouse_helper_position_restore()
        except StopIteration:
            print("No matching taskbar button found - names found:")
            for e in toolbar.children:
                print(f"\t- {e.name}")
            return toolbar