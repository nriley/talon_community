<user.letter>: key(letter)
(ship | uppercase) <user.letters> [(lowercase | sunk | over)]:
    user.insert_formatted(letters, "ALL_CAPS")
<user.symbol_key>: key(symbol_key)
<user.function_key>: key(function_key)
<user.special_key>: key(special_key)
<user.keypad_key>: key(keypad_key)
<user.modifiers> <user.unmodified_key>: key("{modifiers}-{unmodified_key}")
# for key combos consisting only of modifiers, eg. `press super`.
press <user.modifiers>: key(modifiers)
# for consistency with dictation mode and explicit arrow keys if you need them.
press <user.keys>: key(keys)

# Work around a rare word being inserted instead of a key combination in mixed mode
# "manto" instead of "man two"
manto: key(cmd-2)
