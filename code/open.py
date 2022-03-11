from talon import Module, actions

mod = Module()

@mod.action_class
class Actions:
	def file_open():
		"""Open file"""