import re
from collections.abc import Callable
from typing import Optional

from talon import Context, Module, actions, app, ui
from talon.scripting.types import NameDecl

mod = Module()

RE_NON_ALPHA_OR_SPACE = re.compile(r"\s*[^A-Za-z\s]+\s*")


def spoken_forms(s):
    # XXX use user.vocabulary, or may never match
    if RE_NON_ALPHA_OR_SPACE.search(s):
        spoken_forms = "\n".join(
            actions.user.create_spoken_forms(s, generate_subsequences=False)
        )
        return f"""{spoken_forms}
{RE_NON_ALPHA_OR_SPACE.sub(" ", s.lower())}"""
    return s.lower()


def top_left(element):
    if frame := getattr(element, "AXFrame", None):
        return (frame.top, frame.left)
    else:
        return (0, 0)


@mod.action_class
class Actions:
    def ui_dynamic_list_and_capture(
        item_name: str,
        ctx: Context,
        list_decl: NameDecl,
        list_generator: Callable[[], dict[str, ui.Element]],
        element_transformer: Optional[Callable[[ui.Element], object]] = None,
    ):
        """Define a dynamic list and capture to match UI elements.

        item_name: Description of text being matched, for use in errors (e.g. "mailbox name", "section title")
        ctx: Context in which the dynamic list should be defined
        list_decl: List declaration in a module (mod.list(...))
        list_generator: Callable returning a dict mapping str to ui.Element
        element_transformer: Callable mapping a ui.Element in the map above to the capture return value
        """
        LIST = {}
        list_path = list_decl.path
        list_name = list_path.rsplit(".", 1)[1]

        @ctx.dynamic_list(list_path)
        def ui_list(phrase):
            nonlocal LIST

            if not phrase:
                elements = [
                    (*top_left(element), name)
                    for (name, element) in list_generator().items()
                ]
                elements.sort()
                return [name for top, left, name in elements]

            LIST = {
                spoken_forms(name): element
                for name, element in list_generator().items()
            }
            return "\n".join(LIST.keys())

        if element_transformer is None:
            element_transformer = lambda e: e

        def ui_capture(m, element_transformer=element_transformer) -> ui.Element:
            matched_text = getattr(m, list_name)
            if element := LIST.get(matched_text):
                return element_transformer(element)

            for name, element in LIST.items():
                if matched_text in name:
                    return element_transformer(element)

            message = f"No {item_name} containing {matched_text}"
            app.notify(body=message, title=ui.active_app().name)
            raise Exception(message)

        ui_capture.__name__ = list_name
        list_decl.mod.capture(rule=f"{{{list_path}}}")(ui_capture)
