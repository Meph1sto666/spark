from PySide6.QtWidgets import * # type: ignore
from PySide6 import QtCore # type: ignore

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # create a menubar
        menubar:QMenuBar = self.menuBar()
        file_menu:QMenu = menubar.addMenu('File')

        # create a "Open" action
        open_action:QAction = QAction('Open', self)
        open_action.setShortcut('Ctrl+O') # type: ignore
        open_action.triggered.connect(self.open_file_dialog) # type: ignore

        # add the "Open" action to the "File" menu
        file_menu.addAction(open_action)

    def openFileDialog(self) -> None:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog # type: ignore
        filename:str = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)[0] # type: ignore
        if filename:
            print(filename) # type: ignore

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
