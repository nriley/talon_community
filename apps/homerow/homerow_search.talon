tag: user.homerow_search
-
(pick | pic): user.homerow_pick("", false)
(pick | pic) <user.letters>: user.homerow_pick(letters, false)

(pick | pic) and: user.homerow_pick("", true)
(pick | pic) <user.letters> and: user.homerow_pick(letters, true)
