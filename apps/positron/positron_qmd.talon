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

bar assist: user.vscode("quarto-assist.focus")
