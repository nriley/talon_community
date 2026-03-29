app: vscode
-

# Search through Talon or Python files when editing Talon configuration
hunt pie [<user.text>]$: user.vscode_find_everywhere(text or "", "*.py,*.pyi")

hunt talon [<user.text>]$: user.vscode_find_everywhere(text or "", "*.talon")

hunt talon list [<user.text>]$: user.vscode_find_everywhere(text or "", "*.talon-list")

hunt snippet [<user.text>]$: user.vscode_find_everywhere(text or "", "*.snippet")
