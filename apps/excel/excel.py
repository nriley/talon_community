from talon import Context, Module, actions, app, settings

from ...core.edit import edit_command, edit_command_actions

mod = Module()
ctx = Context()

ctx.matches = r"""
app: excel_mac
app: excel_win
"""


@mod.capture(rule="[row] <user.number_string>")
def excel_row(m) -> int:
    return int(m.number_string)


@mod.capture(rule="(column <user.number_string>)|([column] <user.letter>+)")
def excel_column(m) -> str | int:
    if letter := getattr(m, "letter", None):
        return letter.upper()
    return int(m.number_string)


@mod.capture(
    rule="""
        (<user.excel_row> [through <user.excel_row>]) |
        (<user.excel_column> [through (<user.excel_column> | <user.number_string>)]) |
        (<user.excel_row> <user.excel_column> [through <user.excel_row> <user.excel_column>]) |
        (<user.excel_column> <user.excel_row> [through <user.excel_column> <user.excel_row>])
    """
)
def excel_reference(m) -> str:
    match app.platform:
        case "mac":
            from appscript import k

            from .excel_mac import excel_appscript

            R1C1 = excel_appscript().reference_style() == k.R1C1
        case "windows":
            import win32com

            R1C1 = win32com.client.Dispatch("Excel.Application").ReferenceStyle
            R1C1 = R1C1 == -4150

    row = getattr(m, "excel_row", "")
    through_row = getattr(m, "excel_row_2", None)

    if column := getattr(m, "excel_column", None):
        through_column = getattr(
            m, "excel_column_2", getattr(m, "number_string", column)
        )
        if isinstance(column, str):
            if R1C1:
                error = "Excel is configured for R1C1, not A1 reference style"
                app.notify(body=error, title="Excel")
                raise ValueError(error)

            if row:
                if through_row:
                    return f"{column}{row}:{through_column}{through_row}"
                return f"{column}{row}"
            else:
                return f"{column}:{through_column}"
        if not R1C1:
            error = "Excel is configured for A1, not R1C1 reference style"
            app.notify(body=error, title="Excel")
            raise ValueError(error)
        if row:
            if through_row:
                return f"R{row}C{column}:R{through_row}C{through_column}"
            return f"R{row}C{column}"
        return f"C{column}:C{through_column}"
    if through_row:
        return f"R{row}:R{through_row}" if R1C1 else f"{row}:{through_row}"
    return f"R{row}" if R1C1 else f"{row}:{row}"


@mod.action_class
class Actions:
    def excel_save_as_format(format: str):
        """Save Excel document with format"""


def select_lines(action, direction, count):
    if direction == "lineUp":
        selection_callback = actions.edit.extend_line_up
    else:
        selection_callback = actions.edit.extend_line_down

    selection_delay = f"{settings.get('user.edit_command_line_selection_delay')}ms"

    for _attempt in range(1, count + 1):
        selection_callback()
        actions.sleep(selection_delay)

    edit_command_actions.run_action_callback(action)


custom_callbacks = {
    ("delete", "lineUp"): select_lines,
    ("delete", "lineDown"): select_lines,
    ("cutToClipboard", "lineUp"): select_lines,
    ("cutToClipboard", "lineDown"): select_lines,
    ("copyToClipboard", "lineUp"): select_lines,
    ("copyToClipboard", "lineDown"): select_lines,
    ("select", "lineUp"): select_lines,
    ("select", "lineDown"): select_lines,
}


@ctx.action_class("user")
class UserActions:
    def edit_command(action, modifier):
        # XXX Extract functions to actions to make overriding this behavior easier
        # XXX Or consider a "don't extend line when selecting up/down" setting

        if isinstance(modifier, str):
            modifier = edit_command.EditModifier(modifier)
        if isinstance(action, str):
            action = edit_command.EditSimpleAction(action)
        key = (action.type, modifier.type)

        if key in custom_callbacks:
            custom_callbacks[key](action, modifier.type, modifier.count)
            return

        actions.next(action, modifier)
