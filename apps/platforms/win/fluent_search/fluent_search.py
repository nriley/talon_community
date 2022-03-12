from talon import actions, Context, Module

mod = Module()
ctx = Context()

ctx.matches = """
os: windows
"""

@mod.action_class
class Action:
	def fluent_search(text: str):
		"""Searches using Fluent Search"""

@ctx.action_class("user")
class UserActions:
	def fluent_search(text: str):
		# XXX can't use app.focus() and unaware of any other way to
		# automate the way we do with LaunchBar
		# If you have a different search keyboard shortcut configured,
		# replace ctrl-alt-space with it below.
		actions.key('ctrl-alt-space backspace')
		if '\t' in text:
			plugin, text = text.split('\t', 1)
			actions.insert(plugin + '\t')
		actions.user.paste(text)
