from PySide6 import QtWidgets
import PySide6
from PySide6 import QtCore

class AssaDock(QtWidgets.QDockWidget):
	def __init__(self) -> None:
		super().__init__()
		self.setWindowTitle("Screenshot Assistant")
		