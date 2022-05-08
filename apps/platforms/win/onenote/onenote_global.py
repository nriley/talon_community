from talon import Context, actions
from typing import List, Optional

ctx = Context()
ctx.matches = r"""
os: windows
"""

@ctx.action_class('user')
class UserActions:
	def onenote_now(entry: str=""):
		# not standard OneNote; triggers an AutoHotKey macro I wrote
		actions.key("super-alt-i")
		actions.sleep("300ms")
		actions.mimic(entry)
