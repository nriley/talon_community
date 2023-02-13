from talon import Module, actions, ui

mod = Module()


def moom_app():
    return ui.apps(bundle="com.manytricks.Moom")[0]


@mod.action_class
class Actions:
    def moom_key(key: str):
        """Press the corresponding Moom control key"""
        actions.key("ctrl-alt-m")
        actions.sleep("200ms")
        actions.key(key)

    def moom_keys(key: str, times: int = 1):
        """Press the corresponding Moom control key followed by Return"""
        actions.user.moom_key(f"{key}:{times} return")
        actions.sleep("800ms")

    def moom_center_frontmost_window():
        """Tell Moom to center the frontmost window the way macOS would"""
        moom_app().appscript().center_frontmost_window()
