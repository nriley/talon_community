app: sublime_merge
-
tag(): user.command_search
tag(): user.tabs

<user.sublime_merge_pull_with_args>:
    user.sublime_merge_pull(sublime_merge_pull_with_args)

fetch: user.sublime_merge_fetch()
fetch {user.sublime_merge_fetch_arg}+:
    user.sublime_merge_fetch(sublime_merge_fetch_arg_list)

<user.sublime_merge_push_with_args>:
    user.sublime_merge_push(sublime_merge_push_with_args)
