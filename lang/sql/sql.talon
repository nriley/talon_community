tag: user.sql
-
tag(): user.code_operators_math
tag(): user.code_comment_line
tag(): user.code_comment_block_c_like
tag(): user.code_data_null

^select$: "SELECT "
distinct: "DISTINCT "
from: "FROM "
^select star from$: "SELECT *\nFROM "
where: "WHERE "
order by: "ORDER BY "
group by: "GROUP BY "
having: "HAVING "
descending: " DESC"
ascending: " ASC"
dot i d: ".id"
inner join:
    "INNER JOIN  ON "
    key(left:4)
left outer join:
    "LEFT OUTER JOIN  ON "
    key(left:4)
right outer join:
    "RIGHT OUTER JOIN  ON "
    key(left:4)

with:
    key(enter up)
    "WITH  AS ("
    key(enter tab)
    "SELECT "
    key(enter shift-tab)
    edit.extend_line_end()
    edit.delete()
    ") "
    key(delete up:2 right:3)
    
column:
    key(return)
    ", "

count: user.code_insert_function("Count", "")

date:
    "DATE ''"
    key(left)

funk <user.code_functions>:
    user.code_insert_function(code_functions, "")

funk wrap <user.code_functions>:
    user.code_insert_function(code_functions, edit.selected_text())
