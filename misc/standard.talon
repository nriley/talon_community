#(jay son | jason ): "json"
#(http | htp): "http"
#tls: "tls"
#M D five: "md5"
#word (regex | rejex): "regex"
#word queue: "queue"
#word eye: "eye"
#word iter: "iter"
#word no: "NULL"
#word cmd: "cmd"
#word dup: "dup"
#word shell: "shell".
zoom in: edit.zoom_in()
zoom out: edit.zoom_out()
zoom reset: edit.zoom_reset()
scroll up: edit.page_up()
scroll down: edit.page_down()
copy (that | bat): edit.copy()
cut that: edit.cut()
paste that: edit.paste()
clear that: key(backspace)
nope | ((i do | and do | undo) that): edit.undo()
(read do | redo) that: edit.redo()
paste match: edit.paste_match_style()
file open: user.file_open()
file save: edit.save()
#(pad | padding): 
#	insert("  ") 
#	key(left)
slap: edit.line_insert_down()
new paragraph:
	edit.line_end()
	key(enter)
	key(enter)
