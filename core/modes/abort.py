# from https://github.com/AndreasArvidsson/andreas-talon/blob/ed8350b187b6e1e18a93d7ffba451efa3a70bc55/core/on_phrase/abort/abort.py
# and https://github.com/AndreasArvidsson/andreas-talon/blob/ed8350b187b6e1e18a93d7ffba451efa3a70bc55/core/on_phrase/on_phrase.py
# (removing Swedish language context; replacing actions.user.debug with print)

import time

from talon import Module, actions, speech_system
from talon.grammar import Phrase

mod = Module()

ts_threshold: float = None


@mod.action_class
class Actions:
    def abort_current_phrase():
        """Abort current spoken phrase"""
        global ts_threshold
        ts_threshold = time.perf_counter()


def abort_update_phrase(phrase: Phrase) -> tuple[bool, str]:
    """Possibly abort current spoken phrase"""
    global ts_threshold

    words = phrase["phrase"]
    if len(words) == 0:
        return False, ""

    current_phrase = " ".join(words)

    if ts_threshold is not None:
        # Start of phrase is before timestamp threshold
        start = getattr(words[0], "start", phrase["_ts"])
        delta = ts_threshold - start
        ts_threshold = None
        if delta > 0:
            print(f"Aborted phrase: {delta:.2f}s")
            abort_entire_phrase(phrase)
            return True, ""

    return False, current_phrase


def abort_entire_phrase(phrase: Phrase):
    phrase["phrase"] = []
    if "parsed" in phrase:
        phrase["parsed"]._sequence = []


speech_system.register("pre:phrase", abort_update_phrase)
