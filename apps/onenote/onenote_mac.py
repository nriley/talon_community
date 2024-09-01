import re
from enum import Enum
from pathlib import Path

from talon import Context, Module, actions, app, clip, cron, ctrl, ui
from talon.experimental.locate import locate_in_image
from talon.screen import capture
from talon.skia.image import Image

try:
    ui.Element
except AttributeError:  # XXX temporary workaround until this is exposed
    from talon.windows.ax import Element

    ui.Element = Element

mod = Module()
ctx = Context()

mod.apps.onenote_mac = r"""
os: mac
and app.bundle: com.microsoft.onenote.mac
"""

ctx.matches = r"""
app: onenote_mac
"""

MATCHES = __import__("collections").defaultdict(int)


class SidebarTab(Enum):
    NAVIGATION = 0
    SEARCH = 1
    RECENT_NOTES = 2


class NavigationLevel(Enum):
    NOTEBOOKS = -1
    SECTIONS = 0
    PAGES = 1


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.key("ctrl-m")


@ctx.action_class("edit")
class EditActions:
    def copy():
        serial_start = clip.serial()
        for attempt in range(10):
            actions.key("cmd-c")
            actions.sleep("100ms")
            if clip.serial() != serial_start:
                return

    def cut():
        serial_start = clip.serial()
        for attempt in range(10):
            actions.key("cmd-x")
            actions.sleep("100ms")
            if clip.serial() != serial_start:
                return

    def select_line(n: int = None):
        actions.key("right left cmd-a")
        actions.sleep("100ms")

    def paste_match_style():
        text = clip.text()
        with clip.revert():
            clip.set_text(text)
            actions.next()
            actions.sleep("100ms")

    # user.find_and_replace
    def find(text: str = None):
        actions.key("ctrl-g cmd-f")
        actions.sleep("100ms")
        actions.insert(text)


mod.list("onenote_notebooks", desc="Open OneNote notebooks")
mod.list("onenote_sections", desc="Sections in the open OneNote notebook")
mod.list("onenote_pages", desc="Pages in the open OneNote section")


@mod.capture(rule="{user.onenote_notebooks}")
def onenote_notebook(m) -> ui.Element:
    print(f"onenote_notebook {m=}")
    if notebook := ONENOTE_NOTEBOOKS.get(m.onenote_notebooks):
        return notebook.AXParent

    for name, notebook in ONENOTE_NOTEBOOKS.items():
        if m.onenote_notebooks in name:
            return notebook.AXParent

    message = f"No unique notebook title containing “{m.onenote_notebooks}”"
    app.notify(body=message, title="OneNote")
    raise Exception(message)


@mod.capture(rule="{user.onenote_sections}")
def onenote_section(m) -> ui.Element:
    print(f"onenote_section {m=}")
    if section := ONENOTE_SECTIONS.get(m.onenote_sections):
        return section.AXParent

    for name, section in ONENOTE_SECTIONS.items():
        if m.onenote_sections in name:
            return section.AXParent

    message = f"No unique section title containing “{m.onenote_sections}”"
    app.notify(body=message, title="OneNote")
    raise Exception(message)


@mod.capture(rule="{user.onenote_pages}")
def onenote_page(m) -> ui.Element:
    print(f"onenote_page {m=}")
    if page := ONENOTE_PAGES.get(m.onenote_pages):
        return page.AXParent.AXParent.AXParent

    for name, page in ONENOTE_PAGES.items():
        if m.onenote_pages in name:
            return page.AXParent.AXParent.AXParent

    page = f"No unique page title containing “{m.onenote_pages}”"
    app.notify(body=message, title="OneNote")
    raise Exception(message)


@mod.capture(
    rule="<number_small> | <number_small> plus <number_small> | [<number_small>] <user.text>"
)
def now_entry(m) -> str:
    return " ".join(m._unmapped)


@mod.action_class
class Actions:
    def onenote_focus():
        """Bring OneNote to the front"""
        return actions.user.launch_or_focus_bundle("com.microsoft.onenote.mac")

    def onenote_now(entry: str = ""):
        """Insert timestamped bullet list item into OneNote"""
        # XXX work around inability to focus and insert in a single action
        # XXX potentially related to https://github.com/talonvoice/talon/issues/305?
        if actions.user.onenote_focus():
            cron.after("200ms", lambda: actions.user.onenote_now(entry))

    def onenote_font(font: str = ""):
        """Change the font in OneNote"""

    def onenote_font_size(size: int):
        """Change the font size in OneNote (or edit it, if size is 0)"""

    def onenote_font_size_adjust(offset: int):
        """Adjust the font size in OneNote"""

    def onenote_checkbox():
        """Insert indented checkbox into OneNote"""

    def onenote_heading_1():
        """Insert a first-level heading into OneNote"""

    def onenote_hide_navigation():
        """Hide the navigation panes in OneNote"""

    def onenote_hide_ribbon():
        """Hide the Ribbon in OneNote"""

    def onenote_maximize_content_or_press_esc():
        """Hide chrome and zoom content to fit width in OneNote if active, else press Esc"""

    def onenote_copy_link():
        """Copy a link to the current paragraph in OneNote"""

    def onenote_navigate(row_element: ui.Element):
        """Navigate to a OneNote section or page"""

    def onenote_go_progress():
        """Go to the first section of the first notebook"""

    def onenote_go_recent(offset: int):
        """Navigate to recent notes"""

    def onenote_collapse_this():
        """Collapse the current outline in OneNote"""


def onenote_app():
    return ui.apps(bundle="com.microsoft.onenote.mac")[0]


def onenote_notebook_window():
    if not (active_window := ui.active_window()):
        raise Exception("Can't determine active window")

    if active_window.app != onenote_app():
        raise Exception("OneNote is not frontmost")

    if not active_window.doc:
        raise Exception("Frontmost window is not a document window")

    return active_window


def onenote_activate_ribbon_tab(tab_index, tab_name):
    window = onenote_notebook_window()

    ribbon = window.children.find_one(AXRole="AXTabGroup", max_depth=0)
    tab = ribbon.AXTabs[tab_index]
    if tab.get("AXValue") != 1:
        tab.perform("AXPress")

    for attempt in range(10):
        actions.sleep("50ms")
        if tab.get("AXValue") == 1:
            break
    else:
        app.notify(body=f"Could not activate {tab_name} tab", title="OneNote")
        return None

    return ribbon


def onenote_ribbon_combo_box(tab_index, tab_name, box_name, box_filter=None):
    if (ribbon := onenote_activate_ribbon_tab(tab_index, tab_name)) is None:
        return None

    combo_boxes = []
    for attempt in range(10):
        actions.sleep("50ms")
        if combo_boxes := ribbon.children.find(AXRole="AXComboBox"):
            break
    else:
        app.notify(body="Could not find combo boxes", title="OneNote")
        return None

    for combo_box in combo_boxes:
        if combo_box.AXDescription == f"{box_name}:" or box_filter(combo_box):
            return combo_box
    else:
        app.notify(body=f"Could not find {box_name} combo box", title="OneNote")
        return None


def onenote_font_combo_box():
    return onenote_ribbon_combo_box(
        0, "Home", "Font", lambda combo_box: not str.isnumeric(combo_box.AXValue)
    )


def onenote_font_size_combo_box():
    return onenote_ribbon_combo_box(
        0, "Home", "Font Size", lambda combo_box: str.isnumeric(combo_box.AXValue)
    )


def onenote_zoom_combo_box():
    def is_zoom_combo_box(combo_box):
        value = combo_box.AXValue
        return len(value) > 0 and str.isnumeric(value[:-1])

    return onenote_ribbon_combo_box(3, "View", "Zoom", is_zoom_combo_box)


def onenote_image_matches_in_notebook_window(
    window, image_name, attempts=1, delay=None
):
    global MATCHES

    image_dir = Path(__file__).parent / "images"
    if window.screen.scale == 1:
        image_name += "@1x"
    images = {
        image_path.stem: Image.from_file(str(image_path))
        for image_path in sorted(image_dir.glob(f"{image_name}_*.png"))
    }

    for attempt in range(attempts):
        haystack = capture.__self__.capture_window_mac(window.id)

        for image_name, needle in images.items():
            matches = locate_in_image(haystack, needle, threshold=0.99)
            print(attempt, image_name, matches)

            if len(matches) == 1:
                MATCHES[image_name] += 1
                print(sorted(MATCHES.items()))
                return matches

            if len(matches) > 1:
                print(f">1 match for {image_name}: {matches}")

                excess_matches = Path(__file__).parent / "excess_matches"
                excess_matches.mkdir(exist_ok=True)

                now = actions.user.time_format()
                for rect in matches:
                    path = excess_matches / f"{now} {image_name} {rect}.png"
                    capture(*rect, retina=False).write_file(path)

                needle.write_file(excess_matches / f"{now} {image_name}.png")
                haystack.write_file(excess_matches / f"{now} haystack.png")
                return []

            if not matches:
                continue

        if attempt != attempts - 1:
            actions.sleep(delay)

    if not matches:
        print(f"0 matches for {image_name}")

        no_matches = Path(__file__).parent / "no_matches"
        no_matches.mkdir(exist_ok=True)

        now = actions.user.time_format()
        needle.write_file(no_matches / f"{now} {image_name}.png")
        haystack.write_file(no_matches / f"{now} haystack.png")

    return matches


def onenote_show_sidebar(tab):
    window = onenote_notebook_window()
    splitgroup = window.children.find_one(AXRole="AXSplitGroup", max_depth=0)
    group = splitgroup.children.find_one(AXRole="AXGroup", max_depth=0)
    checkbox = group.children.find(AXRole="AXCheckBox", max_depth=0)[tab.value]
    if checkbox.AXValue == 0:
        checkbox.perform("AXPress")
    return splitgroup.children.find_one(AXRole="AXSplitGroup", max_depth=0)


def onenote_notebooks_outline(navigation):
    try:
        sections_pages = navigation.children.find_one(
            AXRole="AXSplitGroup", max_depth=0
        )
    except ui.UIErr:
        pass
    else:
        # sections and pages are visible; show notebooks instead
        notebooks_button = navigation.children.find_one(AXRole="AXButton", max_depth=0)
        notebooks_button.perform("AXPress")

    # wait for notebooks to appear
    for attempt in range(5):
        try:
            notebooks = navigation.children.find_one(AXRole="AXGroup", max_depth=0)
            return notebooks.children.find_one(AXRole="AXOutline")
        except ui.UIErr:
            actions.sleep("100ms")
    else:
        message = "Did not see notebooks as expected"
        app.notify(body=message, title="OneNote")
        raise Exception(message)


RE_NON_ALPHA_OR_SPACE = re.compile(r"\s*[^A-Za-z\s]+\s*")


def spoken_forms(s):
    # XXX use user.vocabulary, or may never match
    if RE_NON_ALPHA_OR_SPACE.search(s):
        return f"""{actions.user.create_spoken_forms(s, generate_subsequences=False)[0]}
{RE_NON_ALPHA_OR_SPACE.sub(" ", s.lower())}"""
    return s.lower()


def onenote_navigation_list(level):
    navigation = onenote_show_sidebar(SidebarTab.NAVIGATION)

    if level == NavigationLevel.NOTEBOOKS:
        outline = onenote_notebooks_outline(navigation)
    else:
        sections_pages = navigation.children.find_one(
            AXRole="AXSplitGroup", max_depth=0
        )
        navigation_levels = sections_pages.children.find(AXRole="AXGroup")
        outline = navigation_levels[level.value].children.find_one(AXRole="AXOutline")

    if level == NavigationLevel.PAGES:
        labels = reversed(outline.children.find(AXRole="AXStaticText"))
        pages = {spoken_forms(label.AXValue): label for label in labels}
        return pages

    cells = reversed(outline.children.find(AXRole="AXCell"))
    notebooks_or_sections = {spoken_forms(cell.AXDescription): cell for cell in cells}
    return notebooks_or_sections


ONENOTE_NOTEBOOKS = {}
ONENOTE_SECTIONS = {}
ONENOTE_PAGES = {}


@ctx.dynamic_list(f"user.onenote_notebooks")
def onenote_notebooks(phrase):
    global ONENOTE_NOTEBOOKS
    print(f"notebook {phrase=}")
    ONENOTE_NOTEBOOKS = onenote_navigation_list(NavigationLevel.NOTEBOOKS)
    return "\n".join(ONENOTE_NOTEBOOKS.keys())


@ctx.dynamic_list(f"user.onenote_sections")
def onenote_sections(phrase):
    global ONENOTE_SECTIONS
    print(f"section {phrase=}")
    ONENOTE_SECTIONS = onenote_navigation_list(NavigationLevel.SECTIONS)
    return "\n".join(ONENOTE_SECTIONS.keys())


@ctx.dynamic_list(f"user.onenote_pages")
def onenote_pages(phrase):
    global ONENOTE_PAGES
    # print(f"page {phrase=}")
    ONENOTE_PAGES = onenote_navigation_list(NavigationLevel.PAGES)
    return "\n".join(ONENOTE_PAGES.keys())


@ctx.action_class("user")
class UserActions:
    # user.find_and_replace
    def find_everywhere(text: str):
        actions.key("ctrl-g cmd-alt-f")
        actions.sleep("200ms")
        actions.insert(text)

    # not standard OneNote; approximate equivalents of AutoHotKey
    def onenote_heading_1():
        actions.key("ctrl-e enter")
        # custom shortcut for "Remove Tag"
        actions.key("cmd-alt-0")
        actions.key("shift-tab:5")
        # neither bullets nor numbering
        actions.key("cmd-. cmd-/ cmd-/")
        # outdent one more time as the above may indent
        actions.key("shift-tab")
        actions.key("cmd-alt-1")

    def onenote_checkbox():
        actions.key("ctrl-e enter tab cmd-1 up ctrl-e")

    def onenote_hide_navigation():
        window = onenote_notebook_window()
        # hide the navigation pane(s) if necessary
        splitgroup = window.children.find_one(AXRole="AXSplitGroup", max_depth=0)
        group = splitgroup.children.find_one(AXRole="AXGroup", max_depth=0)
        try:
            checkbox = group.children.find_one(
                AXRole="AXCheckBox", AXValue=1, max_depth=0
            )
        except ui.UIErr:
            pass
        else:
            checkbox.perform("AXPress")
        # focus the note body if necessary
        for attempt in range(10):
            focused = ui.focused_element()
            if focused and focused.AXRole == "AXWindow" and focused.get("AXDocument"):
                actions.sleep("100ms")
                actions.key("tab")
                actions.sleep("100ms")
            else:
                return
        app.notify(body="Unable to focus note body", title="OneNote")

    def onenote_hide_ribbon():
        window = onenote_notebook_window()

        ribbon = window.children.find_one(AXRole="AXTabGroup", max_depth=0)
        open_tab = ribbon.get("AXValue")
        if open_tab:
            open_tab.perform("AXPress")

    def onenote_maximize_content_or_press_esc():
        if (element := actions.user.focused_element_safe()) is not None:
            app = element.window.app
            if app.bundle != "com.microsoft.onenote.mac":
                ctrl.key_press("esc", app=app)
                return

        actions.user.onenote_hide_ribbon()
        actions.user.onenote_hide_navigation()
        actions.user.zoom_to_fit_width()

    def onenote_go_recent(offset: int):
        navigation = onenote_show_sidebar(SidebarTab.RECENT_NOTES)
        recent_notes = navigation.children.find_one(AXRole="AXGroup", max_depth=0)
        recent_list = recent_notes.children.find_one(AXRole="AXTable", max_depth=1)
        recent_rows = list(recent_list.children.find(AXRole="AXRow", max_depth=0))
        current_row = recent_rows.index(
            next(row for row in recent_rows if row.AXSelected is True)
        )
        desired_row = current_row + offset
        desired_row = max(desired_row, 0)
        desired_row = min(desired_row, len(recent_rows) - 1)
        recent_rows[desired_row].AXSelected = True

    def onenote_navigate(row_element):
        row_element.AXSelected = True

    def onenote_copy_link():
        onenote = onenote_app()
        # despite the name of this menu item, the link takes you directly to the selected paragraph
        (
            onenote.children.find_one(AXRole="AXMenuBar", max_depth=0)
            .children.find_one(AXRole="AXMenuBarItem", AXTitle="Notebooks", max_depth=0)
            .children[0]
            .children.find_one(AXRole="AXMenuItem", AXTitle="Pages", max_depth=0)
            .children[0]
            .children.find_one(
                AXRole="AXMenuItem", AXTitle="Copy Link to Page", max_depth=0
            )
        ).perform("AXPress")
        app.notify(body="Copied link to paragraph", title="OneNote")

    def onenote_go_progress():
        # go to the first notebook
        navigation = onenote_show_sidebar(SidebarTab.NAVIGATION)
        notebooks_outline = onenote_notebooks_outline(navigation)
        first_notebook = notebooks_outline.children.find_one(AXRole="AXRow")
        if not first_notebook.AXSelected:
            first_notebook.AXSelected = True
            actions.key(
                "return"
            )  # XXX auto-dismissal doesn't work when selected via accessibility
        else:
            notebooks_button = navigation.children.find_one(
                AXRole="AXButton", max_depth=0
            )
            notebooks_button.perform("AXPress")

        # wait for section and page navigation to reappear
        for attempt in range(5):
            try:
                sections_pages = navigation.children.find_one(
                    AXRole="AXSplitGroup", max_depth=0
                )
                break
            except ui.UIErr:
                actions.sleep("100ms")
        else:
            app.notify(
                body="Did not see section and page navigation as expected",
                title="OneNote",
            )
            return

        # go to the first section
        sections, pages = (
            child for child in sections_pages.children if child.AXRole == "AXGroup"
        )
        sections_list = sections.children.find_one(AXRole="AXOutline")
        first_section = sections_list.children.find_one(AXRole="AXRow")
        if not first_section.AXSelected:
            first_section.AXSelected = True

    def onenote_now(entry: str = ""):
        actions.key("ctrl-e enter")
        actions.key("cmd-alt-0")  # custom shortcut for "Remove Tag"
        actions.key("cmd-/ cmd-.")
        actions.key("shift-tab:5 tab:2")
        actions.user.insert_time_ampm()
        actions.insert(" - ")
        if entry:
            actions.mimic(entry)

    def onenote_font(font):
        if (combo_box := onenote_font_combo_box()) is None:
            return

        combo_box.AXFocused = True
        if font:
            actions.insert(f"{font}\n")
            actions.key("tab")

    def onenote_font_size(size):
        combo_box = onenote_font_size_combo_box()
        if combo_box is None:
            return

        combo_box.AXFocused = True
        if size:
            combo_box.AXValue = str(size)
            actions.key("return")

    def onenote_font_size_adjust(offset):
        combo_box = onenote_font_size_combo_box()
        if combo_box is None:
            return

        font_size = combo_box.AXValue
        if not str.isnumeric(font_size):
            app.notify(body="Unable to determine current font size", title="OneNote")
            return
        font_size = str(int(font_size) + offset)

        combo_box.AXValue = font_size
        combo_box.AXFocused = True
        actions.key("return")

    def zoom_to_fit_width():
        onenote = onenote_app()
        (
            onenote.children.find_one(AXRole="AXMenuBar", max_depth=0)
            .children.find_one(AXRole="AXMenuBarItem", AXTitle="View", max_depth=0)
            .children[0]
            .children.find_one(
                AXRole="AXMenuItem", AXTitle="Zoom to Page Width", max_depth=0
            )
        ).perform("AXPress")

    def onenote_collapse_this():
        # This code is somewhat fragile, depending on:
        # - Accent color being set to Multicolor (so OneNote's highlight color is lavender)
        # - No other use of the highlight color/outline handle image in the OneNote window
        # - White background for note
        # - 100% zoom level (ensured below)
        # - (Potentially) font size
        window = onenote_notebook_window()
        rect = window.rect
        scale = window.screen.scale

        # Deselect anything and move the mouse pointer out of the way of the content
        # to avoid an accidental match later
        saved_mouse_pos = ctrl.mouse_pos()
        ctrl.mouse_move(rect.x, rect.y)
        actions.edit.right()
        actions.edit.left()

        # Save ribbon state and zoom level
        ribbon = window.children.find_one(AXRole="AXTabGroup", max_depth=0)
        open_tab = ribbon.get("AXValue")

        zoom_combo_box = onenote_zoom_combo_box()
        if zoom_combo_box is None:
            app.notify(
                body=f"Could not find Zoom combo box",
                title="OneNote",
            )
            ctrl.mouse_move(*saved_mouse_pos)
            return
        zoom_level = zoom_combo_box.AXValue
        if zoom_level != "100%":
            actions.edit.zoom_reset()
            actions.sleep("100ms")  # XXX sometimes not long enough to wait
        elif not open_tab:
            # better to do this sooner as it reduces the likelihood of a race
            ribbon.AXValue.perform("AXPress")
        elif open_tab.AXTitle != "View":
            open_tab.perform("AXPress")

        # Select what we are going to collapse into
        actions.edit.select_all()

        matches = onenote_image_matches_in_notebook_window(
            window,
            "onenote_highlight_top_left",
            attempts=10,
            delay="10ms",
        )
        if len(matches) != 1:
            app.notify(
                body=f"Could not find top left corner of highlighted area",
                title="OneNote",
            )
            ctrl.mouse_move(*saved_mouse_pos)
            return

        ctrl.mouse_move(
            rect.x + matches[0].right / scale, rect.y + matches[0].bot / scale
        )

        # XXX Despite everything above, sometimes this is still matching
        # based on the original mouse position - so delay for now
        actions.sleep("100ms")

        matches = onenote_image_matches_in_notebook_window(
            window,
            "onenote_outline_handle_top_left",
            attempts=10,
            delay="10ms",
        )
        if len(matches) == 1:
            ctrl.mouse_move(
                rect.x + matches[0].right / scale, rect.y + matches[0].bot / scale
            )

            actions.sleep("30ms")
            ctrl.mouse_click(button=0)
            ctrl.mouse_click(button=0)
        else:
            app.notify(
                body=f"Could not find top left corner of outline handle",
                title="OneNote",
            )

        ctrl.mouse_move(*saved_mouse_pos)

        # Restore zoom level and ribbon state, if we had to change the zoom level
        if zoom_level != "100%":
            zoom_combo_box.AXValue = zoom_level
            # Usually this takes two tries
            for attempt in range(5):
                zoom_combo_box.AXFocused = True
                if zoom_combo_box.AXFocused == True:
                    actions.key("tab")
                    break
            else:
                app.notify(body=f"Unable to focus zoom combo box", title="OneNote")
            if not open_tab:
                ribbon.AXValue.perform("AXPress")
            elif open_tab.AXTitle != "View":
                open_tab.perform("AXPress")
