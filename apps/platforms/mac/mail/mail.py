from talon import Context, actions, Module, ui

mod = Module()
ctx = Context()

ctx.matches = """
os: mac
and app.bundle: com.apple.mail
"""

def mail_messages_table():
	mail = ui.apps(bundle='com.apple.mail')[0]
	try:
		return mail.active_window.children.find_one(
			AXRole='AXTable', AXDescription='messages', max_depth=3)
	except ui.UIErr:
		return None # no messages table found

@ctx.action_class("user")
class UserActions:
	def mail_select_last_message():
		if not (messages_table := mail_messages_table()):
			return

		last_row = [child for child in messages_table.children if child.AXRole == 'AXRow'][-1]
		last_row.AXSelected = True

	def mail_select_message(offset: int):
		if not (messages_table := mail_messages_table()):
			return

		try: # filtering this way is ~2x as fast as using AXSelectedRows
			selected_row = messages_table.children.find_one(AXSelected=True, max_depth=0)
		except ui.UIErr:
			return

		# index (in all children, not just rows) of first selected row
		desired_index = selected_row.AXIndex + offset
		desired_index = max(desired_index, 0)

		children = list(messages_table.children)
		desired_index = min(desired_index, len(children) - 1)

		# don't get stuck in column headers
		while children[desired_index].AXRole != 'AXRow':
			desired_index += 1
			if desired_index >= len(children):
				return

		children[desired_index].AXSelected = True

@mod.action_class
class Actions:
	def mail_select_last_message():
		"""Select the last message in the currently focused Apple Mail message viewer"""

	def mail_select_message(offset: int):
		"""Navigate to message offset from selected message"""
