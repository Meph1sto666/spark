from lib.types.operator import getPromotionReferenceData, getProfessionReferenceData
from lib.types.misc import *
from lib.expose import *
import pickle

class RefDataPack:
	def __init__(self, imgPath:str, startSize:int, endSize:int) -> None:
		self.profRefData:RefData = getProfessionReferenceData(imgPath,108,150, self.profProgressLogger)
		self.promRefData:RefData = getPromotionReferenceData(imgPath,108,150, self.promProgressLogger)
	
	def profProgressLogger(self, p:float) -> None:
		print("Generating profession ref data", str(round(p, 3)).ljust(7,"0")+"%", end="\r")
	
	def promProgressLogger(self, p:float) -> None:
		print("Generating promotion ref data", str(round(p, 3)).ljust(7,"0")+"%", end="\r")
  
if __name__ == "__main__":
	rfdg = RefDataPack("./userdata/targets/" + os.listdir("./userdata/targets/")[0]) # type: ignore
	pickle.dump(rfdg, open("./userdata/refs/0.srdta", "wb")) # type: ignore
	print()