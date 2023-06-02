import json # type: ignore
from PySide6 import QtWidgets
from PySide6 import QtCore # type: ignore
from ..lang import *

class OpDataDock(QtWidgets.QDockWidget):
	def __init__(self) -> None:
		super().__init__()
		self.language:Lang = Lang("en_us") # NOTE: load from settings
		self.setWindowTitle("Data Viewer")
		# self.setStyleSheet(open("./data/styles/data_dock.css", "r").read())
		self.table = QtWidgets.QTableWidget()
		self.table.setColumnCount(0)
		self.table.setRowCount(1)
		self.table.setMinimumWidth(1000)
		self.layout().addWidget(self.table)
		# self.table.show()
		self.table.setMinimumHeight(self.height())

		self.lens:list[int] = [0,0,0,0,0,0,0,0,0]
		
	def addData(self, data:list[dict[str, str | int | list[int] | dict[str, str | int | None] | None]]) -> None:
		# print(data)
		keys = list(data[0].keys())
		for i in range(len(keys)): self.table.setItem(0, i, QtWidgets.QTableWidgetItem(keys[i]))
		self.table.setColumnCount(len(data[0].keys()))
		for i in range(len(data)):
			self.table.setRowCount(self.table.rowCount()+1)
			for j in range(len(keys)):
				dta: str | int | list[int] | dict[str, str | int | None] | None = data[i].get(keys[j], "")
				if type(dta) in [list]:
					item = QtWidgets.QTableWidgetItem(" ".join([f"S{d+1} M{dta[d]}" for d in range(len(dta))])) # type: ignore
				elif type(dta) in [dict]:
					item = QtWidgets.QTableWidgetItem(f'{dta["type"]} S{dta["stage"]}') # type: ignore
				else:
					item = QtWidgets.QTableWidgetItem(str(dta))
					# if dta == False:
				if self.lens[j] < len(item.text()):
					self.lens[j] = len(item.text())
				self.table.setItem(self.table.rowCount()-1, j, item)
		for j in range(len(self.lens)):
			self.table.setColumnWidth(j, self.lens[j]*9)
				