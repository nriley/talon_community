from talon import Module, Context

ctx = Context()
mod = Module()

ctx.matches = r"""
os: mac
"""

@ctx.action_class("user")
class UserActions:
	def fantastical_parse(text: str):
		ui.apps(bundle='com.flexibits.fantastical2.mac')[0].appscript().parse_sentence(text)

	def fantastical_show_mini_calendar():
		import webbrowser
		webbrowser.open(f"x-fantastical3://show/mini")

	def fantastical_show_calendar():
		import webbrowser
		webbrowser.open(f"x-fantastical3://show/calendar")

@mod.action_class
class Actions:
	def fantastical_parse(text: str): """Parses the text in Fantastical."""
	def fantastical_show_mini_calendar(): """Shows the mini calendar popover."""
	def fantastical_show_calendar(): """Shows the calendar window."""
