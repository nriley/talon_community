import re
import time
from collections.abc import Callable
from typing import Optional

from talon import Context, Module, actions, app, settings, ui
from talon.scripting.types import NameDecl

mod = Module()

# Dynamic selection list processing can get slow when processing lots of text.
# On my M4 Max, it's about 170K chars/sec.  Some apps will put a LOT into
# accessibility descriptions which may not even be visible to the user.
mod.setting(
    "ui_spoken_form_max_characters",
    type=str,
    default=0,
    desc="The maximum number of characters to process in a UI element label (0 for no limit)",
)

RE_NON_ALPHA_OR_SPACE = re.compile(r"\s*[^A-Za-z\s]+\s*")
RE_SPACE = re.compile(r"\s+")


def spoken_forms(s, max_length=0):
    # XXX use user.vocabulary, or may never match
    s = str(s)
    if max_length and len(s) > max_length:
        if str.isspace(s[max_length - 1]):
            s = s[: max_length - 1]
        elif str.isspace(s[max_length]):
            s = s[:max_length]
        else:
            rest_of_word = RE_SPACE.split(s[max_length:], maxsplit=1)[0]
            s = s[: (max_length + len(rest_of_word))]
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
        LIST_GENERATION_TIME = None
        LIST_GENERATION_END_TIME = None
        list_path = list_decl.path
        list_name = list_path.rsplit(".", 1)[1]

        @ctx.dynamic_list(list_path)
        def ui_list(phrase):
            nonlocal LIST, LIST_GENERATION_TIME, LIST_GENERATION_END_TIME

            if not phrase:
                elements = [
                    (*top_left(element), str(name))
                    for (name, element) in list_generator().items()
                ]
                elements.sort()
                return [name for top, left, name in elements]

            max_length = settings.get("user.ui_spoken_form_max_characters")
            start_time = time.time()
            LIST = {
                spoken_forms(name, max_length): element
                for name, element in list_generator().items()
            }
            LIST_GENERATION_END_TIME = time.time()
            LIST_GENERATION_TIME = LIST_GENERATION_END_TIME - start_time
            return "\n".join(LIST.keys())

        if element_transformer is None:

            def element_transformer(e):
                return e

        def ui_capture(m, element_transformer=element_transformer) -> ui.Element:
            processing_time = time.time() - LIST_GENERATION_END_TIME
            if LIST_GENERATION_TIME > 0.1 or processing_time > 0.1:
                list_length = len("\n".join(LIST.keys()))
                print(
                    f"dynamic list generation time {LIST_GENERATION_TIME:.2f}s; length {list_length} characters; recognition time {processing_time:.2f}s"
                )

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
