mode: sleep
os: windows
-
# prevent talon from walking up super easily in sleep mode at the moment with wav2letter
# (see sleep_mode.talon - per aegis this is specifically for gen2)
<phrase>: skip()
