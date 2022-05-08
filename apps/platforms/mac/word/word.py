from talon import Module, Context, actions
from talon.mac import applescript

ctx = Context()
mod = Module()

ctx.matches = r"""
app: word_mac
"""

@ctx.action_class('user')
class UserActions:
	def find(text: str):
		actions.key('cmd-f')
		if text:
			actions.insert(text)

	def find_next(): actions.key('cmd-g')
	def find_previous(): actions.key('cmd-shift-g')

	def find_everywhere(text: str):
		actions.user.menu_select('Edit|Find|Advanced Find and Replace...')
		if text:
			actions.insert(text)

	def find_toggle_match_by_case(): pass # could implement
	def find_toggle_match_by_word(): pass
	def find_toggle_match_by_regex(): pass

	def replace(text: str):
		actions.user.menu_select('Edit|Find|Replace...')
		if text:
			actions.insert(text)
	replace_everywhere = replace

	def replace_confirm(): pass
	def replace_confirm_all(): pass

	def select_previous_occurrence(text: str):
		actions.edit.find(text)
		actions.edit.find_previous()
		actions.key('esc')

	def select_next_occurrence(text: str):
		actions.edit.find(text)
		actions.edit.find_next()
		actions.key('esc')
