from talon import Module, actions, app, ui

mod = Module()


@mod.action_class
class Actions:
    def shroud_ensure_running() -> bool:
        """Launch Shroud if necessary; return if Shroud was running"""
        shroud_bundle = "net.sabi.Shroud"
        if len(ui.apps(bundle=shroud_bundle)):
            return True

        ui.launch(bundle=shroud_bundle)
        for attempt in range(50):
            if len(ui.apps(bundle=shroud_bundle)):
                return False
            actions.sleep("50ms")

        app.notify("Unable to launch Shroud")
        return False

    def shroud_focus_app():
        """Focus the frontmost app with Shroud"""
        if actions.user.shroud_ensure_running():
            actions.key("ctrl-alt-a")
