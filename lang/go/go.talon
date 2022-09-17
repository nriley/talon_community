tag: user.go
-
tag(): user.code_imperative

tag(): user.code_comment_line
tag(): user.code_comment_block_c_like
tag(): user.code_data_bool
tag(): user.code_data_null
tag(): user.code_functions
tag(): user.code_functions_common
tag(): user.code_libraries
tag(): user.code_libraries_gui
tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_math
tag(): user.code_operators_pointer

settings():
    user.code_private_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_function_formatter = "PUBLIC_CAMEL_CASE"
    user.code_private_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_variable_formatter = "PUBLIC_CAMEL_CASE"

variadic: "..."

# Many of these add extra terrible spacing under the assumption that
# gofmt/goimports will erase it.

state var: "var "
variable [<user.text>] [over]:
    insert("var ")
    insert(user.formatted_text(text, "PRIVATE_CAMEL_CASE"))
    # insert(" ")
    sleep(100ms)

state (chan | channel): " chan "
state go: "go "
spawn <user.text> [over]:
    insert("go ")
    insert(user.formatted_text(text, "PRIVATE_CAMEL_CASE"))

state format: "fmt"
format <user.text> [over]:
    insert("fmt.")
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))

state select: "select "
# "select <user.text>:insert("select "), insert(user.formatted_text(text, "PRIVATE_CAMEL_CASE")]
state (const | constant): " const "
constant <user.text> [over]:
    insert("const ")
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))

state type: " type "
type <user.text> [over]:
    insert("type ")
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))

state (start | struct | struck):
    insert(" struct {")
    key("enter")
(struct | struck) <user.text> [over]:
    insert(" struct {")
    key("enter")
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))

[state] empty interface: " interface{} "
state interface:
    insert(" interface {")
    key("enter")
interface <user.text> [over]:
    insert(" interface {")
    key("enter")
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))

state slice: " []"
slice of: "[]"
[state] (no | nil): "nil"
state (int | integer | ant) sixty four: " int64 "
state tag: user.insert_between(" `", "`")
field tag <user.text> [over]:
    user.insert_between(" `", "`")
    sleep(100ms)
    insert(user.formatted_text(text, "snake"))
    insert(" ")
    sleep(100ms)

map of string to string: " map[string]string "
map of <user.text> [over]:
    insert("map[")
    insert(user.formatted_text(text, "PRIVATE_CAMEL_CASE"))
    key("right")
    sleep(100ms)

receive: " <- "
make: "make("
loggers [<user.text>] [over]:
    insert("logrus.")
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))

length [<user.text>] [over]:
    insert("len(")
    insert(user.formatted_text(text or "", "PRIVATE_CAMEL_CASE"))

append <user.text> [over]:
    insert("append(")
    insert(user.formatted_text(text, "PRIVATE_CAMEL_CASE"))

state (air | err): "err"
error: " err "
loop over [<user.text>] [over]:
    insert("forr ")
    insert(user.formatted_text(text, "PRIVATE_CAMEL_CASE"))

item <user.text> [over]:
    insert(", ")
    insert(user.formatted_text(text, "PRIVATE_CAMEL_CASE"))

value <user.text> [over]:
    insert(": ")
    insert(user.formatted_text(text, "PRIVATE_CAMEL_CASE"))

swipe [<user.text>] [over]:
    key("right")
    insert(", ")
    insert(user.formatted_text(text, "PRIVATE_CAMEL_CASE"))
