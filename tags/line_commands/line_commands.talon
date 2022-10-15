tag: user.line_commands
-
#this defines some common line commands. More may be defined that are ide-specific.
lend: edit.line_end()
bend: edit.line_start()
go <number>: edit.jump_line(number)
go <number> end:
    edit.jump_line(number)
    edit.line_end()
comment [line] <number>:
    user.select_range(number, number)
    code.toggle_comment()
comment <number> through <number>:
    user.select_range(number_1, number_2)
    code.toggle_comment()
clear [line] <number>:
    edit.jump_line(number)
    user.select_range(number, number)
    edit.delete()
clear <number> through <number>:
    user.select_range(number_1, number_2)
    edit.delete()
copy [line] <number>:
    user.select_range(number, number)
    edit.copy()
copy <number> through <number>:
    user.select_range(number_1, number_2)
    edit.copy()
cut [line] <number>:
    user.select_range(number, number)
    edit.cut()
cut <number> through <number>:
    user.select_range(number_1, number_2)
    edit.cut()
(paste | replace) <number> through <number>:
    user.select_range(number_1, number_2)
    edit.paste()
(select | cell | sell) [line] <number>: user.select_range(number, number)
(select | cell | sell) <number> through <number>: user.select_range(number_1, number_2)
move right: edit.indent_more()
move right <number>:
    edit.jump_line(number)
    edit.indent_more()
move right <number> through <number>:
    user.select_range(number_1, number_2)
    edit.indent_more()
move left: edit.indent_less()
move left <number>:
    user.select_range(number, number)
    edit.indent_less()
move left <number> through <number>:
    user.select_range(number_1, number_2)
    edit.indent_less()
move down: edit.line_swap_down()
move up: edit.line_swap_up()
move up <number>:
    user.select_range(number, number)
    edit.line_swap_up()
move up <number> through <number>:
    user.select_range(number_1, number_2)
    edit.line_swap_up()
move down <number>:
    user.select_range(number, number)
    edit.line_swap_down()
move down <number> through <number>:
    user.select_range(number_1, number_2)
    edit.line_swap_down()
clone (line | that): edit.line_clone()
clone [line] <number>:
    user.select_range(number, number)
    edit.select_line()
    edit.line_clone()
    key(left)

clear camel left: user.delete_camel_left()
clear camel right: user.delete_camel_right()
select camel left: user.extend_camel_left()
select camel right: user.extend_camel_right()
go camel left: user.camel_left()
go camel right: user.camel_right()
