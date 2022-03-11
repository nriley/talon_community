from talon import actions, app, Context, Module, ui

import subprocess

mod = Module()
ctx = Context()
ctx.matches = r"""
os: mac
"""

mod.list('shortcuts', desc='Shortcuts')
ctx.lists['user.shortcuts'] = {}

@mod.action_class
class Actions:
	def shortcuts_refresh():
		"""Refresh the list of shortcuts"""

	def shortcut_run(shortcut: str) -> str:
		"""Run a shortcut"""

@ctx.action_class('user')
class UserActions:
	def shortcuts_refresh():
		refresh()

	def shortcut_run(shortcut: str) -> str:
		return subprocess.check_output(['/usr/bin/shortcuts', 'run', shortcut]).decode()

def refresh():
	shortcuts = subprocess.check_output(['/usr/bin/shortcuts', 'list']).decode().split('\n')
	shortcuts = actions.user.create_spoken_forms_from_list(shortcuts)

	ctx.lists['user.shortcuts'] = shortcuts

if app.platform == 'mac':
	app.register('ready', refresh)

