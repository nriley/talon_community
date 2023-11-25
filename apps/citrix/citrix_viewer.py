from talon import Context, Module, actions, clip, ui

ctx = Context()
mod = Module()

mod.apps.citrix_viewer = """
os: mac
and app.bundle: com.citrix.receiver.icaviewer.mac
"""

ctx.matches = """
app: citrix_viewer
"""


def citrix_view_menu():
    citrix_viewer = ui.active_app()
    if citrix_viewer.bundle != "com.citrix.receiver.icaviewer.mac":
        print("Citrix Viewer is not the active application")
        return None
    menu_bar = citrix_viewer.children.find_one(AXRole="AXMenuBar", max_depth=0)
    view_menu = menu_bar.children.find_one(
        AXRole="AXMenuBarItem", AXTitle="View", max_depth=0
    ).children[0]
    return view_menu


@ctx.action_class("user")
class UserActions:
    def window_toggle_full_screen():
        view_menu = citrix_view_menu()
        menu_items = view_menu.children.find(AXRole="AXMenuItem", max_depth=0)

        if full_screen_item := next(
            (
                item
                for item in menu_items
                if item.AXTitle in ("Enter Full Screen", "Exit Full Screen")
            ),
            None,
        ):
            full_screen_item.perform("AXPress")
        else:
            print(
                "Unable to find Citrix Viewer full screen menu item (non-English localization?)"
            )

    def citrix_use_all_displays_in_full_screen():
        view_menu = citrix_view_menu()
        use_all_displays_in_full_screen_item = view_menu.children.find_one(
            AXRole="AXMenuItem", AXTitle="Use All Displays In Full Screen", max_depth=0
        )
        use_all_displays_in_full_screen_item.perform("AXPress")


@ctx.action_class("app")
class AppActions:
    def window_close():
        actions.key("alt-f4")

    def window_next():
        actions.key("alt-tab")

    def window_previous():
        actions.key("alt-shift-tab")


@ctx.action_class("edit")
class EditActions:
    def selected_text() -> str:
        pass

        clip.set_text("blah")
        # clip.clear()
        actions.edit.copy()
        # old_formats = []
        for i in range(15):
            # print(i, clip.mime().formats, clip.text())
            # if clip.mime().formats != old_formats: # clip.text() != 'blah':
            # 	old_formats = clip.mime().formats
            # 	print('formats', old_formats, 'in', i*10, 'ms')
            # elif clip.text():
            # 	print('text', clip.text(), 'in', i*10, 'ms')
            if clip.text() != "blah":
                break
            actions.sleep("10ms")
        else:
            return ""
        return clip.text()

        # from time import perf_counter
        # from talon.api import ffi, lib, ffi_string
        # # print('manual before', ffi_string(lib.tl_clipboard_get_text(lib.TL_CLIP_MAIN)))
        # print('text', clip.text())
        # if hasattr(clip, 'mime'):
        # 	try: print('mime', clip.mime().text)
        # 	except: print('no mime text', clip.mime().formats)
        # 	print('before', clip.mime().formats)
        # start = perf_counter()
        # text = actions.next()
        # end = perf_counter()
        # print(f'selected_text |{text}| in {end - start}s')
        # print('text', clip.text())
        # # actions.sleep('2s')
        # if hasattr(clip, 'mime'):
        # 	try: print('mime', clip.mime().text)
        # 	except: print('no mime text', clip.mime().formats)
        # 	print('after', clip.mime().formats)
        # print("manual", ffi_string(lib.tl_clipboard_get_text(lib.TL_CLIP_MAIN)))

        return text


@mod.action_class
class Actions:
    def window_toggle_full_screen():
        """Toggle full screen state of the frontmost window"""

    def citrix_use_all_displays_in_full_screen():
        """Toggle using all displays in full screen"""
