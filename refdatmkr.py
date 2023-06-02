import cv2
from lib.types.operator import getPromotionReferenceData, getProfessionReferenceData
from lib.types.misc import *
import pickle

class RefDataCreator:
	def __init__(self, img:cv2.Mat) -> None:
		self.profRefData:RefData = getProfessionReferenceData(img,108,150, self.profProgressLogger)
		self.promRefData:RefData = getPromotionReferenceData(img,108,150, self.promProgressLogger)
	
	def profProgressLogger(self, p:float) -> None:
		print("Generating profession ref data", str(round(p, 3)).ljust(7,"0")+"%", end="\r")
	
	def promProgressLogger(self, p:float) -> None:
		print("Generating promotion ref data", str(round(p, 3)).ljust(7,"0")+"%", end="\r")
  
if __name__ == "__main__":
	rfdg = RefDataCreator(cv2.imread("./userdata/targets/" + os.listdir("./userdata/targets/")[0]))
	pickle.dump(rfdg, open("./userdata/refs/0.srdta", "wb")) # type: ignore
	print()