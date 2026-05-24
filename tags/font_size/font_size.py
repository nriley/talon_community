from typing import Optional

from talon import Module, actions

mod = Module()
mod.tag("font_size", desc="Tag for enabling font size commands")


@mod.action_class
class Actions:
    def get_font_size() -> float:
        """Return the font size"""

    def set_font_size(size: Optional[float] = 0):
        """Change the font size (or edit it, if size is 0/omitted)"""

    def adjust_font_size(offset: float):
        """Adjust the font size by the specified offset"""
        font_size = actions.user.get_font_size()
        actions.user.set_font_size(font_size + offset)
