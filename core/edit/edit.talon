# Compound of action(select, clear, copy, cut, paste, etc.) and modifier(word, line, etc.) commands for editing text.
# eg: "select line", "clear all"
<user.edit_action> <user.edit_modifier>: user.edit_command(edit_action, edit_modifier)

# XXX Workaround for likely core Talon issue in which "clear line" doesn't work even
# though it's defined in the captures/underlying lists above (and works with sim/mimic);
# seems to be related to the clear [line] <number> command in line_commands.talon
clear line: edit.delete_line()

# Zoom
zoom in: edit.zoom_in()
zoom out: edit.zoom_out()
zoom reset: edit.zoom_reset()

# Searching
hunt this: edit.find()
^hunt this <user.text>$: edit.find(text)

hunt next: edit.find_next()
hunt previous: edit.find_previous()

# Navigation

# The reason for these spoken forms is that "page up" and "page down" are globally defined as keys.
scroll up: edit.page_up()
scroll down: edit.page_down()

go west: edit.word_left()
go east: edit.word_right()

# go left, go left left down, go 5 left 2 down
# go word left, go 2 words right
go <user.navigation_step>+: user.perform_navigation_steps(navigation_step_list)

go line start | head: edit.line_start()
go line end | tail: edit.line_end()

go paragraph start: edit.paragraph_start()
go paragraph end: edit.paragraph_end()

go way left:
    edit.line_start()
    edit.line_start()
go way right: edit.line_end()
go way up: edit.file_start()
go way down: edit.file_end()

go top: edit.file_start()
go bottom: edit.file_end()

go page up: edit.page_up()
go page down: edit.page_down()

# Selecting

select left: edit.extend_left()
select right: edit.extend_right()
select up: edit.extend_line_up()
select down: edit.extend_line_down()

select (word left | west): edit.extend_word_left()
select (word right | east): edit.extend_word_right()

select way left: edit.extend_line_start()
select way right: edit.extend_line_end()
select way up: edit.extend_file_start()
select way down: edit.extend_file_end()

# Indentation
indent [more]: edit.indent_more()
(indent less | out dent): edit.indent_less()

# Delete
clear left: edit.delete()
clear right: user.delete_right()

clear up:
    edit.extend_line_up()
    edit.delete()

clear down:
    edit.extend_line_down()
    edit.delete()

clear (word (left | previous) | west):
    edit.extend_word_left()
    edit.delete()

clear (word (right | next) | east):
    edit.extend_word_right()
    edit.delete()

clear way left:
    edit.extend_line_start()
    edit.delete()

clear way right:
    edit.extend_line_end()
    edit.delete()

clear way up:
    edit.extend_file_start()
    edit.delete()

clear way down:
    edit.extend_file_end()
    edit.delete()

# Copy
copy that: edit.copy()
copy (word left | west): user.copy_word_left()
copy (word right | east): user.copy_word_right()

#to do: do we want these variants, seem to conflict
# copy left:
#      edit.extend_left()
#      edit.copy()
# copy right:
#     edit.extend_right()
#     edit.copy()
# copy up:
#     edit.extend_up()
#     edit.copy()
# copy down:
#     edit.extend_down()
#     edit.copy()

# Cut
cut that: edit.cut()
cut (word left | west): user.cut_word_left()
cut (word right | east): user.cut_word_right()

#to do: do we want these variants
# cut left:
#      edit.select_all()
#      edit.cut()
# cut right:
#      edit.select_all()
#      edit.cut()
# cut up:
#      edit.select_all()
#     edit.cut()
# cut down:
#     edit.select_all()
#     edit.cut()

# Paste
(pace | pist | paste) (that | it): edit.paste()
(pace | pist | paste) enter:
    edit.paste()
    key(enter)
(pace | pist | paste) match: edit.paste_match_style()

# Duplication
clone that: edit.selection_clone()
clone line: edit.line_clone()

# Insert new line
insert up | new line above: edit.line_insert_up()
insert down | new line below | slap: edit.line_insert_down()

new paragraph:
    edit.line_end()
    key(enter)
    key(enter)

# Insert padding with optional symbols
(pad | padding): user.insert_between(" ", " ")
(pad | padding) <user.symbol_key>+:
    insert(" ")
    user.insert_many(symbol_key_list)
    insert(" ")

# Undo/redo
nope | undo that: edit.undo()
redo that: edit.redo()

# Open
file open: user.file_open()

# Save
file save: edit.save()
file save all: edit.save_all()

[go] line mid: user.line_middle()
