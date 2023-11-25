from appscript import k
from appscript.reference import CommandError
from talon import Context, actions, ui
from talon.mac import applescript

ctx = Context()
ctx.matches = r"""
app: finder
"""


def finder():
    return ui.apps(bundle="com.apple.finder")[0].appscript()


@ctx.action_class("user")
class UserActions:
    def file_manager_open_parent():
        actions.key("cmd-up")

    def file_manager_go_forward():
        actions.key("cmd-]")

    def file_manager_go_back():
        actions.key("cmd-[")

    def file_manager_current_path():
        if ui.active_window().title == "":
            return None  # likely a modal window
        try:
            return applescript.run(
                r"""
                tell application id "com.apple.Finder"
                    with timeout of 0.1 seconds
                        if not (exists (front Finder window's target)) then return
                        if front Finder window's target's class is not in {disk, folder} then return
                        get front Finder window's target
                        return (result as alias)'s POSIX path
                    end timeout
                end tell
            """
            )
        except applescript.ApplescriptErr as e:
            print(
                f'Unable to get path of frontmost Finder window "{ui.active_window().title}": {e}'
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
        """opens the directory that's already visible in the view"""
        escaped_path = path.replace(r'"', r"\"")
        applescript.run(
            f"""
            set _folder to POSIX file "{escaped_path}"

            tell application id "com.apple.finder"
                try
                    with timeout of 0.1 seconds
                        if (front Finder window's target exists) and (front Finder window's sidebar width > 0) then
                            set front Finder window's target to _folder
                            return
                        end if
                    end timeout
                end try
                open _folder
            end tell
        """
        )

    def file_manager_select_directory(path: str):
        """selects the directory"""
        actions.insert(path)

    def file_manager_new_folder(name: str):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        actions.key("cmd-shift-n")
        actions.sleep("500ms")
        actions.insert(name)

    def file_manager_open_file(path: str):
        """opens the file"""
        actions.key("esc")
        actions.insert(path)
        actions.key("cmd-o")

    def file_manager_select_file(path: str):
        """selects the file"""
        actions.key("esc")
        actions.insert(path)
