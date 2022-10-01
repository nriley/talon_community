os: windows
-
settings():
    # record everything to ~/.talon/recordings
    speech.record_all = 0
    # seems I get cut off more often on Windows
    speech.timeout = 0.2
