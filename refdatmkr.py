from lib.types.operator import getPromotionReferenceData, getProfessionReferenceData
from lib.types.misc import *
from lib.expose import *
import pickle


	
def profProgressLogger(p:float) -> None:
	print("Generating profession ref data", str(round(p, 3)).ljust(7,"0")+"%", end="\r")
	
def promProgressLogger(p:float) -> None:
	print("Generating promotion ref data", str(round(p, 3)).ljust(7,"0")+"%", end="\r")
  
if __name__ == "__main__":
	path = "./userdata/targets/" + os.listdir("./userdata/targets/")[0]
	profRefData:RefData = getProfessionReferenceData(path, 108, 150, profProgressLogger) # 30
	promRefData:RefData = getPromotionReferenceData(path, 108, 150, promProgressLogger) # 30
	pickle.dump(profRefData, open("./userdata/refs/prf.srd", "wb"))
	pickle.dump(promRefData, open("./userdata/refs/prm.srd", "wb"))
	print()