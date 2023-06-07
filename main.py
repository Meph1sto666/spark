import sys # type: ignore
from lib.gui.main_window import * # type: ignore
 # type: ignore
# img:cv2.Mat = cv2.imread("./testdata/0.png") # type: ignore
app = QtWidgets.QApplication(sys.argv) # type: ignore
# app.setStyleSheet(open("./data/styles/dark_theme.css").read()) # type: ignore
window = MainWindow() # type: ignore
window.setMinimumHeight(500) # type: ignore
window.setMinimumWidth(888) # type: ignore
window.show() # type: ignore
app.exec() # type: ignore