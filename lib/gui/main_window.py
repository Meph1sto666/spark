from PySide2 import QtWidgets
from lib.gui.analyser import *
from PySide2 import QtCore

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self) -> None:
		super().__init__()

		self.analyser = OpAnalyserDock()
		self.analyser.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.analyser)