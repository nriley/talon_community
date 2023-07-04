app: vscode
-
# Search through Talon or Python files when editing Talon configuration
hunt pie [<user.text>]$:
    user.find_everywhere(text or "")
    key(tab:5)
    "*.py,*.pyi"
    key(shift-tab:5)

hunt talon [<user.text>]$:
    user.find_everywhere(text or "")
    key(tab:5)
    "*.talon"
    key(shift-tab:5)
