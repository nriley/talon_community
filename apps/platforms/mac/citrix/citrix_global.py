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
			# XXX work around the subrole being AXDialog when the app is hidden
			was_hidden = viewer.element.AXHidden
			if was_hidden is True:
				viewer.element.AXHidden = False
			for window in viewer.windows():
				if window.element.get('AXSubrole') == 'AXStandardWindow':
					viewer.focus()
					window.focus()
					return
			if was_hidden:
				viewer.element.AXHidden = True

