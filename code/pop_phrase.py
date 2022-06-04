# from mankoff on Talon Slack

from talon import Context, Module, actions, app, noise, speech_system, ui

ctx = Context()
mod = Module()

last_phrase = ""
pop_phrase = ""

auto_pop_that_phrases = ["go", "move", "select", "undo that", "cursor more"]


def on_phrase(j):
    """Record the last phrase"""
    global last_phrase
    if not (text := j.get("text")):
        return
    phrase = " ".join(text)
    last_phrase = phrase
    # auto-set pop_phrase if the last phrase is in the auto_pop_that_phrases list

    global auto_pop_that_phrases
    for p in auto_pop_that_phrases:
        if phrase[0 : len(p)] == p:
            global pop_phrase
            pop_phrase = phrase
            return
    else:
        pop_phrase = ""


speech_system.register("post:phrase", on_phrase)


@mod.action_class
class Actions:
    def pop_phrase():
        """Set pop command to the last phrase"""
        global last_phrase
        global pop_phrase
        pop_phrase = last_phrase
        print(f"*** Setting pop phrase: {pop_phrase} ***")


def on_pop(active):
    global pop_phrase
    if pop_phrase == "":
        return
    actions.mimic(pop_phrase)


noise.register("pop", on_pop)


def ui_event(event, arg=None):
    global pop_phrase
    pop_phrase = ""


def on_ready():
    ui.register("app_activate", ui_event)
    ui.register("win_focus", ui_event)


app.register("ready", on_ready)
