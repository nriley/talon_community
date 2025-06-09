app: positron
-
notebook new: user.vscode("quarto.newNotebook")
quarto new: user.vscode("quarto.fileNewDocument")

panel console: user.vscode("workbench.action.positronConsole.focusConsole")

sec (viewer | preview): user.vscode("workbench.panel.positronPreview.focus")
sec help: user.vscode("workbench.panel.positronHelp.focus")
sec variables: user.vscode("positronVariables.focus")
sec plots: user.vscode("workbench.panel.positronPlots.focus")

help that: user.vscode("positron.help.showHelpAtCursor")
