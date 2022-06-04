from talon import Module, actions

mod = Module()


@mod.action_class
class Actions:
    def moom_key(key: str):
        """Press the corresponding Moom control key."""
        actions.key("ctrl-alt-m")
        actions.sleep("200ms")
        actions.key(key)

    def moom_keys(key: str, times: int = 1):
        """Press the corresponding Moom control key followed by Return."""
        actions.user.moom_key(f"{key}:{times} return")
        actions.sleep("800ms")
