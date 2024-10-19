from talon import Module, actions, app, ui

mod = Module()


def wait_focused_app(bundle, tries=10):
    for attempt in range(tries):
        active_app = ui.active_app()
        if active_app.bundle == bundle:
            return active_app
        try:
            active_app = ui.focused_element().window.app
            if active_app.bundle == bundle:
                return active_app
        except (RuntimeError, OSError, ui.UIErr):
            pass
        actions.sleep("50ms")
    else:
        return None


@mod.action_class
class Actions:
    def launch_bundle(bundle: str):
        """Launch an application by bundle ID."""
        ui.launch(bundle=bundle)

    def focus_bundle(bundle: str):
        """Focus and return an application by bundle ID, or None if unable to do so."""
        active_app = ui.active_app()
        if active_app.bundle == bundle:
            return active_app
        try:
            ui.apps(bundle=bundle)[0].focus()
        except IndexError:
            return None

        if (focused_app := wait_focused_app(bundle)) is None:
            app.notify(title="Failed to focus application", body=f"Bundle ID: {bundle}")
        return focused_app

    def launch_or_focus_bundle(bundle: str):
        """Launch or focus and return an application by bundle ID, or None if unable to do so."""
        if (focused_app := actions.user.focus_bundle(bundle)) is not None:
            return focused_app

        actions.user.launch_bundle(bundle)
        if (focused_app := wait_focused_app(bundle, tries=100)) is not None:
            return focused_app

        return actions.user.focus_bundle(bundle)
