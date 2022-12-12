from talon import Context, actions, noise, registry

ctx = Context()

ctx.matches = """
mode: sleep
"""


def on_pop(active):
    if ctx not in registry.active_contexts():
        return
    if actions.user.fd_is_listening():
        return
    if actions.user.dictation_suspended():
        return
    actions.user.disable_fd()
    actions.speech.enable()
    print("+ Enabled speech on pop")


noise.register("pop", on_pop)
