from talon import Module, actions

mod = Module()

@mod.action_class
class Actions:
	def zoom_to_fit():
		"""Zoom to fit"""

	def zoom_to_fit_width():
		"""Zoom to fit width"""
		actions.user.zoom_to_fit()

	def zoom_to_fit_height():
		"""Zoom to fit height"""
		actions.user.zoom_to_fit()

	def zoom_to_selection():
		"""Zoom to selection"""
