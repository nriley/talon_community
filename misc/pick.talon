# select from a list with the keyboard
pick: key(return)
pick <number_small>:
	key("down:{number_small - 1}")
	sleep(10ms)
	key(return)
