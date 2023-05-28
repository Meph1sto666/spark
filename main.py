from PySide2 import QtWidgets
import os

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self) -> None:
		super().__init__()

  
		self.imgSelect = QtWidgets.QComboBox(self)
		self.imgSelect.addItems(os.listdir("./testdata/"))
		self.imgSelect.setMaximumHeight(30)
		self.setCentralWidget(self.imgSelect)
		self.imgSelect.currentIndexChanged.connect(self.on_combo_box_changed)

		
	def on_combo_box_changed(self, index:int) -> None:
		print('Selected index:', index)
		print('Selected text:', self.imgSelect.currentText())

if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	window = MainWindow()
	window.show()
	app.exec_()
