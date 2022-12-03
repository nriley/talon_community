from talon import Context, actions, noise

ctx = Context()

ctx.matches = """
mode: sleep
"""


def on_pop(active):
    actions.user.disable_fd()
    actions.speech.toggle()


noise.register("pop", on_pop)
