from talon import actions, app, scope, ui, Module, Context

mod = Module()
ctx = Context()
ctx.matches = """
os: windows
"""

@mod.action_class
class Actions:
	def reselect_microphone():
		"""Reselect microphone (workaround for Talon bug on Windows) if speech is active"""

@Context().action_class('user')
class FallbackUserActions:
	def reselect_microphone(): pass

@ctx.action_class('user')
class UserActions:
	def reselect_microphone():
		if 'sleep' in scope.get('mode'):
			return

		active_microphone = actions.sound.active_microphone()
		if active_microphone == "None":
			return

		actions.sound.set_microphone("None")
		actions.sound.set_microphone(active_microphone)

def ui_callback(event, app):
	if event not in ('app_launch', 'app_close'):
		return
	if app.exe or app.name != 'LogonUI.exe':
		return
	if event == "app_launch":
	    actions.speech.disable()
	    return

	print(event, app)

if app.platform == "windows":
	ui.register("", ui_callback)
