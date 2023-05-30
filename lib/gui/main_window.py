from PySide6 import QtWidgets
from lib.gui.analyser import *
from lib.gui.assa_dock import *
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6.QtWidgets import QSystemTrayIcon
import ctypes

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self) -> None:
		super().__init__()
		appIcon = QtGui.QIcon("./assets/icon_180.png")
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("just why")
		QSystemTrayIcon(appIcon, parent=self).show()
		self.setWindowIcon(appIcon)
		self.setWindowTitle("SpectArk")
		
		self.analyser = OpAnalyserDock()
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.analyser) # type: ignore
		self.assaDock = AssaDock()
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.assaDock) # type: ignore
		self.setStyleSheet(open("./data/layout.css").read())