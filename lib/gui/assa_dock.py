import json
from PySide6 import QtWidgets
from PySide6 import QtCore # type: ignore
from ..lang import *

class AssaDock(QtWidgets.QDockWidget):
	def __init__(self) -> None:
		super().__init__()
		self.language:Lang = Lang("en_us") # NOTE: load from settings
		self.setWindowTitle("Screenshot Assistant")
		self.setStyleSheet(open("./data/styles/assa_dock.css", "r").read())

		self.emuSelector = QtWidgets.QComboBox(self)
		for k in json.load(open("./data/emulators.json", "r")):
			self.emuSelector.addItem(self.language.translate(k), k)
		self.emuSelector.currentIndexChanged.connect(self.emuSelectCb)

		self.autoFullScreen = QtWidgets.QCheckBox(self.language.translate("assa_afs_checkbox"))
		self.autoFullScreen.setToolTip(self.language.translate("assa_afs_checkbox_tt"))
		self.layout().addWidget(self.autoFullScreen)

		# self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self) # type: ignore
		# self.layout().addWidget(self.slider)
		
		# self.titleBarWidget().setStyleSheet(open("./data/styles/dock_bar.css").read())

		
	def emuSelectCb(self, index:int) -> None:
		self.emulator:str = self.emuSelector.itemData(index)
		print(self.emulator)
