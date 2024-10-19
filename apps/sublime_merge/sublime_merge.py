from re import sub
from typing import Optional

from talon import Context, Module, actions, app, ui

mod = Module()

mod.apps.sublime_merge_mac = r"""
os: mac
and app.bundle: com.sublimemerge
"""

mod.apps.sublime_merge_win = r"""
os: windows
and app.exe: sublime_merge.exe
"""

mod.apps.sublime_merge = r"""
app: sublime_merge_mac
app: sublime_merge_win
"""

mod.list("sublime_merge_fetch_arg", desc="Argument to fetch in Sublime Merge")


def matched_args(m, all_args):
    arg_words = str(m)
    args = []
    for words, arg in all_args.items():
        if words in arg_words:
            args.append(arg)
    return args or None


sublime_merge_pull_args = {
    "f f only": "--ff-only",
    "re base": "--rebase",
    "auto stash": "--autostash",
}


@mod.capture(rule="pull [(f f only | re base)] [auto stash]")
def sublime_merge_pull_with_args(m) -> Optional[list[str]]:
    return matched_args(m, sublime_merge_pull_args)


sublime_merge_push_args = {
    "force with lease": "--force-with-lease",
    "force": "--force",
    "no verify": "--no-verify",
}


@mod.capture(rule="push [(force [with lease])] [no verify]")
def sublime_merge_push_with_args(m) -> Optional[list[str]]:
    return matched_args(m, sublime_merge_push_args)


@mod.action_class
class Actions:
    def sublime_merge_fetch(args: Optional[list[str]] = None):
        """Fetch changes in Sublime Merge"""

    def sublime_merge_pull(args: Optional[list[str]] = None):
        """Pull changes in Sublime Merge"""

    def sublime_merge_push(args: Optional[list[str]] = None):
        """Push changes in Sublime Merge"""


ctx = Context()
ctx.matches = r"""
app: sublime_merge
"""

ctx.lists["user.sublime_merge_fetch_arg"] = {
    arg: f"--{arg}" for arg in ("all", "prune", "tags")
}


@ctx.action_class("user")
class UserActions:
    def sublime_merge_fetch(args=None):
        actions.key("shift-f7")
        actions.insert(f"fetch {' '.join(args) if args else ''}")
        actions.key("enter")

    def sublime_merge_pull(args):
        if not args:
            actions.key("cmd-alt-down" if app.platform == "mac" else "ctrl-alt-down")
            return
        actions.key("shift-f7")
        actions.insert(f"{' '.join(args)}")
        actions.key("enter")

    def sublime_merge_push(args):
        if not args:
            actions.key("cmd-alt-up" if app.platform == "mac" else "ctrl-alt-up")
            return
        actions.key("shift-f8")
        actions.insert(f"{' '.join(args)}")
        actions.key("enter")
