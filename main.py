import sys
from lib.gui.main_window import *

# img:cv2.Mat = cv2.imread("./testdata/0.png")
app = QtWidgets.QApplication(sys.argv)
# app.setStyleSheet(open("./data/styles/dark_theme.css").read())
window = MainWindow()
window.setMinimumHeight(500)
window.setMinimumWidth(888)
window.show()
app.exec()