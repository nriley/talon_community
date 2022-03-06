from talon import Context, Module, ui

mod = Module()
ctx = Context()

ctx = Context()
ctx.matches = """
os: mac
"""

@mod.action_class
class Action:
	def citrix_focus_desktop():
		"""Focus the Citrix desktop"""

@ctx.action_class("user")
class UserActions:
	def citrix_focus_desktop():
		for viewer in ui.apps(bundle='com.citrix.receiver.icaviewer.mac'):
			for window in viewer.windows():
				if window.element.AXSubrole == 'AXStandardWindow':
					window.focus()
					return
