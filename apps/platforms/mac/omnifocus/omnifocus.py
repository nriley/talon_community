from typing import Optional

from talon import Context, actions, Module
from talon.mac import applescript

mod = Module()
ctx = Context()

ctx.matches = """
os: mac
and app.bundle: com.omnigroup.OmniFocus3.MacAppStore
"""

@ctx.action_class("user")
class UserActions:
	def omnifocus_complete():
		applescript.run("""tell application id "com.omnigroup.OmniFocus3.MacAppStore"
			set _content to window 1's content
			set _selectedTrees to _content's selected trees
			mark complete (_content's selected trees's value)
			set _content's selected trees to _selectedTrees
		end tell""")

	def omnifocus_postpone(days: Optional[int]):
		actions.key("ctrl-cmd-l")
		if days:
			actions.insert(str(days))

	def omnifocus_select_tree(tree: str):
		applescript.run(f'tell application id "com.omnigroup.OmniFocus3.MacAppStore" to tell window 1\'s content to set selected trees to {{{tree}}}')
		actions.key("alt-cmd-2")

	def find_everywhere(text: str):
		actions.key("alt-cmd-f")
		actions.insert(text)

@mod.action_class
class Actions:
	def omnifocus_complete():
		"""Mark the selection as completed while preserving the selection"""

	def omnifocus_postpone(days: Optional[int]):
		"""Postpone by a number of days"""

	def omnifocus_select_tree(tree: str):
		"""Select a tree in the outline (specified as AppleScript scoped to window content)"""
