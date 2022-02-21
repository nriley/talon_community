from talon import Module, Context, actions, app, ui
from talon.mac import applescript

ctx = Context()
mod = Module()

ctx.matches = r"""
app: excel_mac
"""

@ctx.action_class('edit')
class EditActions:
	def zoom_in():
		applescript.run(r"""
			tell application id "com.microsoft.Excel" to set front window's zoom to (front window's zoom) * 1.25
		""")

	def zoom_out():
		applescript.run(r"""
			tell application id "com.microsoft.Excel" to set front window's zoom to (front window's zoom) / 1.25
		""")

	def zoom_reset():
		applescript.run(r"""
			tell application id "com.microsoft.Excel" to set front window's zoom to 100
		""")

def excel_app():
	return ui.apps(bundle="com.microsoft.Excel")[0]

def excel_window():
	return next(window for window in excel_app().windows() if window.doc or window.title)

@ctx.action_class('user')
class UserActions:
	def excel_save_as_format(format: str):
		actions.key('cmd-shift-s')
		window = excel_window()

		for attempt in range(5):
			try:
				sheet = window.children.find_one(AXRole='AXSheet', max_depth=0)
				break
			except ui.UIErr:
				actions.sleep("100ms")
		else:
			app.notify(body='Did not find save sheet as expected', title='Excel')
			return

		file_format_popup = sheet.children.find_one(AXRole='AXPopUpButton', AXDescription='File Format:')
		file_format_popup.perform('AXPress')

		for attempt in range(5):
			try:
				file_format_menu = file_format_popup.children.find_one(AXRole='AXMenu', max_depth=0)
				break
			except ui.UIErr:
				actions.sleep("100ms")
		else:
			app.notify(body='Did not find file format menu as expected', title='Excel')
			return

		file_format_item = file_format_menu.children.find_one(AXRole='AXMenuItem', AXTitle=format, max_depth=0)
		file_format_item.perform('AXPress')

@mod.action_class
class Actions:
	def excel_save_as_format(format: str):
		"""Save Excel document with format"""
