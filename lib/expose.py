import typing
import eel
from lib.types.operator import *
from lib.settings import * 

def prfrdCallbackConvert(originalPath:str, startSize:int, endSize:int) -> None:
	profrefdta:RefData = getProfessionReferenceData(originalPath,startSize,endSize, eel.callback)
	pickle.dump(profrefdta, open("./userdata/refs/prf.srd", "wb"))
def prmrdCallbackConvert(originalPath:str, startSize:int, endSize:int) -> None:
	promrefdta:RefData = getPromotionReferenceData(originalPath,startSize,endSize, eel.callback)
	pickle.dump(promrefdta, open("./userdata/refs/prm.srd", "wb"))


	
functions:list[typing.Callable[..., typing.Any]] = [
	getPromotionReferenceData,
	getProfessionReferenceData,
	getBool,
	setBool,
	getString,
	setString,
	getNum,
	setNum,
	prfrdCallbackConvert,
	prmrdCallbackConvert
]
def exposeAll() -> None:
	for f in functions:
		eel.expose(f) # type: ignore

