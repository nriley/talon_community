os: mac
and app.bundle: com.apple.Preview
-
settings():
    user.ocr_select_with_drag = 1

previous: key(alt-up)
next: key(alt-down)

go <number>:
    key(cmd-alt-g)
    insert("{number}")
    key(enter)
