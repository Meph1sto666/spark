from PySide2.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # create a menubar
        menubar:QMenuBar = self.menuBar()
        file_menu:QMenu = menubar.addMenu('File')

        # create a "Open" action
        open_action:QAction = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file_dialog)

        # add the "Open" action to the "File" menu
        file_menu.addAction(open_action)

    def openFileDialog(self) -> None:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename:str = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)[0]
        if filename:
            print(filename)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
