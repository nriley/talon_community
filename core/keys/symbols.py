# fmt: off

# define the spoken forms for symbols in command and dictation mode
punctuation_dict = {}

# for dragon, we add a couple of mappings that don't work for conformer
# i.e. dragon supports some actual symbols as the spoken form
dragon_punctuation_dict = {
    "`": "`",
    ",": ",",
}

# define the spoken forms for symbols that are intended for command mode only
symbol_key_dict = {}

# define spoken form for symbols for use in create_spoken_forms.py functionality
# we define a handful of symbol only. at present, this is restricted to one entry per symbol.
symbols_for_create_spoken_forms = {
    # for application names like "Movies & TV"
    "and": "&",
    # for emails
    "at": "@",
    "dot": ".",
    # for application names like "notepad++"
    "plus": "+",
}


class Symbol:
    character: str
    command_and_dictation_forms: list[str] = None
    command_forms: list[str] = None

    def __init__(
        self, character: str, command_and_dictation_forms=None, command_forms=None
    ):
        self.character = character

        if command_and_dictation_forms:
            self.command_and_dictation_forms = (
                [command_and_dictation_forms]
                if isinstance(command_and_dictation_forms, str)
                else command_and_dictation_forms
            )

        if command_forms:
            self.command_forms = (
                [command_forms] if isinstance(command_forms, str) else command_forms
            )

currency_symbols = [
    Symbol("$", ["dollar sign"], ["dollar"]),
    Symbol("£", ["pound sign"], ["pound"]),
]

symbols = [
    Symbol("`", ["back tick"]),
    Symbol(",", ["comma", "coma", "come a"]),
    Symbol(".", ["period"], ["dot", "point"]),
    Symbol(";", ["semicolon"], ["semi"]),
    Symbol(":", ["colon"]),
    Symbol("?", ["question mark"], ["question"]),
    Symbol("!", ["exclamation mark", "exclamation point"], ["bang"]),
    Symbol("*", ["asterisk"], ["star"]),
    Symbol("#", ["number sign"], ["number"]),
    Symbol("%", ["percent sign"], ["percent"]),
    Symbol("@", ["at sign"]),
    Symbol("&", ["ampersand"]),
    Symbol("-", ["hyphen"], ["minus", "dash"]),
    Symbol("–", ["en dash"]),
    Symbol("—", ["em dash"]),
    Symbol("=", None, ["equals"]),
    Symbol("+", None, ["plus"]),
    Symbol("~", None, ["tilde"]),
    Symbol("_", None, ["score", "underscore"]),
    Symbol("(", ["open paren"], ["paren"]),
    Symbol(")", ["close paren"], None),
    Symbol("[", ["open bracket"], ["square"]),
    Symbol("]", ["close bracket"], ["close square"]),
    Symbol("/", ["slash"]),
    Symbol("\\", None, ["backslash", "whack"]),
    Symbol("{", ["open curly bracket"], ["brace"]),
    Symbol("}", ["close curly bracket"], ["close brace"]),
    Symbol("<", ["less than"], ["angle"]),
    Symbol(">", ["greater than"], ["rangle"]),
    Symbol("^", None, ["caret"]),
    Symbol("|", None, ["pipe"]),
    Symbol("'", None, ["quote", "apostrophe"]),
    Symbol('"', None, ["dub quote"]),
]

# by convention, symbols should include currency symbols
symbols.extend(currency_symbols)

for symbol in symbols:
    if symbol.command_and_dictation_forms:
        for spoken_form in symbol.command_and_dictation_forms:
            punctuation_dict[spoken_form] = symbol.character
            symbol_key_dict[spoken_form] = symbol.character
            dragon_punctuation_dict[spoken_form] = symbol.character

    if symbol.command_forms:
        for spoken_form in symbol.command_forms:
            symbol_key_dict[spoken_form] = symbol.character
