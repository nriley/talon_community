try:
    from appscript import k
    from appscript.aem.mactypes import File
    from appscript.reference import CommandError
except ImportError:
    pass

import os.path

from talon import Context, Module, actions, app, ui

mod = Module()
ctx = Context()
ctx.matches = r"""
app: finder
"""


def finder():
    return ui.apps(bundle="com.apple.finder")[0].appscript()


@mod.action_class
class Actions:
    def finder_open_trash():
        """Open the Trash in the Mac Finder"""


@ctx.action_class("user")
class UserActions:
    def finder_open_trash():
        finder().trash.open()

    def file_manager_open_parent():
        actions.key("cmd-up")

    def file_manager_current_path():
        if ui.active_window().title == "":
            return None  # likely a modal window
        try:
            target = finder().Finder_windows[1].target
            if not target.exists(timeout=0.1):
                return None
            if target.class_(timeout=0.1) not in {k.disk, k.folder}:
                return None
            return target.get(resulttype=k.alias, timeout=0.1).path
        except CommandError:  # fails with some windows, e.g. AirDrop window
            print(
                f'Unable to get path of frontmost Finder window "{ui.active_window().title}"'
            )

    def file_manager_terminal_here():
        if ui.active_window().title == "":
            return  # likely a modal window
        try:
            target = (
                finder().Finder_windows[1].target.get(resulttype=k.alias, timeout=0.1)
            )
        except CommandError:
            return  # fails with some windows, e.g. AirDrop window

        terminal = actions.user.launch_or_focus_bundle(
            bundle="com.apple.Terminal"
        ).appscript()
        terminal.open(target)

    def file_manager_show_properties():
        """Shows the properties for the file"""
        actions.key("cmd-i")

    def file_manager_open_directory(path: str):
        """Opens the directory (that's already visible in the view, if needed)"""

        finder_app = finder()
        front_window = finder_app.Finder_windows[1]
        if front_window.target.exists(timeout=0.1) and front_window.sidebar_width() > 0:
            front_window.target.set(front_window.target.folders[path])
            return

        if not os.path.isabs(path):
            path = os.path.join(actions.user.file_manager_current_path(), path)
        path_ref = File(path)
        finder_app.open(path_ref)

    def file_manager_select_directory(path: str):
        """selects the directory"""
        finder_app = finder()
        front_window = finder_app.Finder_windows[1]
        if not front_window.target.exists(timeout=0.1):
            return
        finder_app.selection.set(front_window.target.folders[path])

    def file_manager_new_folder(name: str):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        finder_app = finder()
        try:
            new_folder = finder_app.make(
                new=k.folder,
                at=finder_app.insertion_location(),
                with_properties={k.name: name},
            )
        except CommandError as e:
            app.notify(f"Unable to create folder named “{name}”", e.errormessage)
            return
        finder_app.select(new_folder)

    def file_manager_open_file(path: str):
        """opens the file"""
        actions.key("esc")
        actions.insert(path)
        actions.key("cmd-o")

    def file_manager_select_file(path: str):
        """selects the file"""
        actions.key("esc")
        actions.insert(path)

    def address_focus():
        actions.key("cmd-shift-g")

    def address_copy_address():
        actions.key("alt-cmd-c")

    def address_navigate(address: str):
        actions.user.file_manager_open_directory(address)
