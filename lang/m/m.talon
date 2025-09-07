code.language: m
-
tag(): user.code_functions_common
tag(): user.code_imperative
tag(): user.code_keywords
tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_math
tag(): user.code_operators_pointer

op {user.code_operators_m}: user.code_operator(code_operators_m)

funk: "$$"
select: user.insert_snippet_by_name("switchStatement")
set: user.insert_between("s ", "=")
when: ":"
