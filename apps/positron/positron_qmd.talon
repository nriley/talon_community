app: positron
win.file_ext: .qmd
-

cell: user.vscode("quarto.insertCodeCell")
cell next: user.vscode("quarto.goToNextCell")
cell previous: user.vscode("quarto.goToPreviousCell")

cell run: user.vscode("quarto.runCurrentCell")
[cell run] advance: user.vscode("quarto.runCurrentAdvance")
cell run all: user.vscode("quarto.runAllCells")
run: user.vscode("quarto.runCurrent")
preview: user.vscode("quarto.preview")

# This command is exposed as "Quarto: Show Assist Panel" and "Focus on Quarto View"
# and if a panel tab, it's labeled "Explorer". So, support all of these for now.
# By default it's in the primary side bar, so allow "bar".
[bar] (assist | quarto | explorer): user.vscode("quarto-assist.focus")
