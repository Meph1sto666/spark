from PySide2 import QtWidgets

class OpAnalyserDock(QtWidgets.QDockWidget):
	def __init__(self) -> None:
		super().__init__()
		self.startBtn = QtWidgets.QToolButton(self)
		self.startBtn.clicked.connect(self.startCb) # type: ignore
		

	def startCb(self) -> None:
		print("start")