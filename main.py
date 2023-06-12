import eel
import cv2
from lib.types.operator import *
from lib.expose import exposeAll

eel.init("./src/") # type: ignore
exposeAll()
eel.start("index.html", mode="firefox") # type: ignore