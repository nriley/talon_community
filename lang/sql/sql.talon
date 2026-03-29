code.language: sql
-

tag(): user.code_operators_math
tag(): user.code_comment_line
tag(): user.code_comment_block_c_like
tag(): user.code_comment_line
tag(): user.code_data_null
tag(): user.code_functions_common
tag(): user.code_imperative
tag(): user.code_keywords
tag(): user.code_operators_math

inner join: user.insert_between("INNER JOIN ", " ON ")
inner join using: user.insert_between("INNER JOIN ", " USING ")
left outer join: user.insert_between("LEFT OUTER JOIN ", " ON ")
right outer join: user.insert_between("RIGHT OUTER JOIN ", " ON ")

exists: user.insert_between("EXISTS (", ")")

with: user.insert_snippet_by_name("withStatement")

column:
    edit.line_insert_down()
    insert(", ")

count: user.code_insert_function("Count", "")

date: user.insert_between("DATE '", "'")
