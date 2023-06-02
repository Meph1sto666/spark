from PySide6 import QtWidgets
from lib.gui.analyser import *
from lib.gui.assa_dock import *
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6.QtWidgets import QSystemTrayIcon
import ctypes
from ..lang import *
from lib.gui.data_dock import *
from lib.types.operator import *

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self) -> None:
		super().__init__()
		self.language:Lang = Lang("en_us") # NOTE: load from settings
		appIcon = QtGui.QIcon("./data/assets/icon_180.png")
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("just why")
		QSystemTrayIcon(appIcon, parent=self).show()
		self.setWindowIcon(appIcon)
		self.setWindowTitle("SpectArk")
		
		# self.analyser = OpAnalyserDock()
		# self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.analyser) # type: ignore
		self.assaDock = AssaDock()
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.assaDock) # type: ignore
		# print(open("./data/styles/dark_theme.css").read()+"\n"+open("./data/styles/main.css").read())
		# self.setStyleSheet(open("./data/styles/main.css").read())

		self.dataDock = OpDataDock()
		self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dataDock) # type: ignore
		for o in os.listdir("./userdata/saves"):
			self.dataDock.addData([load(os.path.splitext(o)[0]).toJson()])