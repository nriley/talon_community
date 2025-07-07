from talon import Module, app

mod = Module()

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
            from talon.mac import applescript # XXX convert to appscript

            R1C1 = applescript.run(
                """tell application id "com.microsoft.Excel" to get (reference style is R1C1)"""
            )
            R1C1 = R1C1 == "true"
        case "windows":
            import win32com
            R1C1 = win32com.client.Dispatch('Excel.Application').ReferenceStyle
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
