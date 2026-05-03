from talon import Context, Module

mod = Module()
ctx = Context()

mod.apps.mame = r"""
os: mac
and app.bundle: org.mamedev.mame
"""

ctx.matches = r"""
os: mac
app: mame
"""
