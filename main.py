import sys
from lib.gui.main_window import *

# img:cv2.Mat = cv2.imread("./testdata/0.png")
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.setMinimumHeight(500)
window.setMinimumWidth(888)
window.show()
app.exec()