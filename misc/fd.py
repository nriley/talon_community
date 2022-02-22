from talon import Module, actions

import sys

fda = None

if sys.platform == 'win32':
	import win32api
	import win32com.client

	# needed? On Win10, this is in C:\ProgramData\MModal\DesktopDictationClient\Versions\[...]
	win32api.SetDllDirectory(r'C:\MModal\Server')
	fda = win32com.client.Dispatch("FDLink.Application")

mod = Module()

@mod.action_class
class Actions:
	def fd_is_running() -> bool:
		"""Is Fluency Direct running?"""
		if fda is None:
			return False
		return fda.IsRunning()

	def disable_fd():
		"""Disable Fluency Direct"""
		if fda is None:
			return

		if not actions.user.fd_is_running():
			return

		fdas = fda.Connect()
		if fdas is None:
			return # unable to connect

		# this just turns on/off dictation; leaves commands enabled
		# fddc = fdas.GetDictationControl()
		# fddc.SetEnabled(True)

		# can't enable from FD UI while recording is disabled
		fdrc = fdas.GetRecordingControl()
		fdrc.EnableRecording(False)
		# however, recording remains off after reenabled
		fdrc.EnableRecording(True)

	def enable_fd():
		"""Enable Fluency Direct via a keyboard shortcut."""
		if not actions.user.fd_is_running():
			return
		# start out with FD in a known state
		actions.user.disable_fd()
		actions.key("`")
