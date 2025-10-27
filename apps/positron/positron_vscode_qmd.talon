# Adding Quarto Markdown Support For Positron and VSCode
app: vscode
app: positron
win.file_ext: .qmd
-

# Quarto Markdown
cell: user.vscode("quarto.insertCodeCell")
cell next: user.vscode("quarto.goToNextCell")
cell previous: user.vscode("quarto.goToPreviousCell")

# Run cell
cell run: user.vscode("quarto.runCurrentCell")
[cell run] advance: user.vscode("quarto.runCurrentAdvance")
cell run next: user.vscode("quarto.runNextCell")
cell run last: user.vscode("quarto.runPreviousCell")

# Run notebook
notebook run head: user.vscode("quarto.runCellsAbove")
notebook run tail: user.vscode("quarto.runCellsBelow")
notebook run: user.vscode("quarto.runAllCells")

run [that]: user.vscode("quarto.runCurrent")

[quarto] preview: user.vscode("quarto.previewScript")

go to [<user.text>]:
    user.vscode("workbench.action.gotoSymbol")
    insert(text)

# This command is exposed as "Quarto: Show Assist Panel" and "Focus on Quarto View"
# and if a panel tab, it's labeled "Explorer". So, support all of these for now.
# By default it's in the primary side bar, so allow "bar".
[bar] (assist | quarto | explorer): user.vscode("quarto-assist.focus")
