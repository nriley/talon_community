from talon import Context, Module, actions, ui

mod = Module()
ctx = Context()

mod.apps.apple_music = r"""
os: mac
and app.bundle: com.apple.Music
"""

ctx.matches = r"""
os: mac
app: apple_music
"""


def apple_music_app():
    return ui.apps(bundle="com.apple.Music")[0]


@mod.action_class
class Actions:
    def media_shuffle():
        """Shuffles the currently selected media"""


@ctx.action_class("user")
class UserActions:
    def media_shuffle():
        from appscript import k

        music = apple_music_app().appscript()
        music.stop()
        music.shuffle_mode.set(k.songs)
        music.shuffle_enabled.set(True)
        music.play()
