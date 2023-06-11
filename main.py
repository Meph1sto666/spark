import eel
import cv2
from lib.types.operator import *

eel.init("./src/") # type: ignore

@eel.expose # type: ignore
def loadImg() -> cv2.Mat:
	i:cv2.Mat = cv2.imread("./userdata/targets/Screenshot_2023.06.02_18.23.53.122.png", cv2.IMREAD_UNCHANGED)
	# Image.fromarray(i).show()
	return i

eel.start("index.html", mode="firefox") # type: ignore