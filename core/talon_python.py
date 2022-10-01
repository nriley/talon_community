from talon import Context

ctx = Context()
ctx.matches = r"""
tag: user.talon_python
"""


@ctx.action_class("code")
class CodeActions:
    def language():
        return "python"
