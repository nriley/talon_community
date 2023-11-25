app: word_win
-
# tag(): user.find_and_replace

paste special: key(cmd-ctrl-v)

align left: key(ctrl-l)
align center: key(ctrl-e)

bold: key(ctrl-b)
italic: key(ctrl-i)
underline: key(ctrl-u)
# strike through: key(ctrl-shift-x)

mail this:
    user.office_tell_me()
    "Mail Recipient (As Attachment)"
    sleep(1s)
    key(enter)

ribbon: key(ctrl-f1)
