from talon import Module, Context, actions

ctx = Context()
mod = Module()

ctx.matches = r"""
os: mac
"""

@ctx.action_class("user")
class UserActions:
	def launchbar_action(action: str, argument: str):
		import appscript
		app = appscript.app(id='at.obdev.LaunchBar')
		if argument:
			app.perform_action(action, with_string=argument)
		else:
			app.perform_action(action)

	def launchbar_select(text: str):
		from urllib.parse import quote
		import webbrowser
		abbreviation = actions.user.formatted_text(text, "ALL_LOWERCASE,NO_SPACES")
		webbrowser.open('x-launchbar:select?abbreviation=' + quote(abbreviation))

@mod.action_class
class Actions:
	def launchbar_action(action: str, argument: str):
		"""Performs the LaunchBar action with an (optional) specified argument"""

	def launchbar_select(text: str):
		"""Selects an abbreviation in LaunchBar"""
