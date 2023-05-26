import os
import json
from lib.types.errors import *
import cv2

class RefData:
	def __init__(self, conf:float, size:int, x:int, y:int) -> None:
		self.conf: float = conf
		self.size: int = size
		self.x: int = x
		self.y: int = y
	def toTuple(self) -> tuple[float, int, int, int]:
		return (self.conf, self.size, self.x, self.y)

def drawBoundingBox(image:cv2.Mat,x:int,y:int,w:int,h:int,text:str|None=None, inset:bool=False) -> cv2.Mat:
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) # type: ignore
	if text != None:
		cv2.putText(image, text, (x, (y - 10) if not inset else (y + 30)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2) # type: ignore
	return image
def bgraToRgba(img:cv2.Mat) -> cv2.Mat:
	return cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
def rgbaToBgra(img:cv2.Mat) -> cv2.Mat:
	return cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
def toGrayscale(image:cv2.Mat) -> cv2.Mat:
	return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def filterNamesByProfession(c:str) -> list[str]:
	ops:list[dict[str, str]] = dict(json.load(open("./ref/class2op.json"))).get(c, [])
	return [o["name"] for o in ops]
def filterAvatarsByProfession(c:str) -> list[str]:
	ops:list[dict[str, str]] = json.load(open("./ref/class2op.json")).get(c)
	opIds:list[str] = [o.get("id", "None").split("_")[1] for o in ops]
	return list(filter(lambda x: x.split("_")[1] in opIds, os.listdir("./ref/avatars/")))
def getIdByName(name:str) -> str:
	ops:dict[str,dict[str,str]] = json.load(open("./ref/operators.json"))
	id:str|None = list(filter(lambda o: o[1].get("name")==name, ops.items()))[0][1].get("id", None)
	if id == None:
		raise OperatorNameNotFound()
	return id
def getSkinsById(id:str) -> list[str]:
	return [os.path.splitext(s)[0] for s in filter(lambda f: id in f, os.listdir("./ref/avatars/"))]

def filterNamesByRarity(r:int) -> list[str]:
	ops:dict[str,dict[str,int|str]] = json.load(open("./ref/operators.json"))
	return [str(n[1].get("name")) for n in list(filter(lambda o: o[1].get("rarity")==r, ops.items()))]
def filterNamesByRarityAndProfession(r:int, p:str) -> list[str]:
	ops:dict[str,dict[str,int|str]] = json.load(open("./ref/operators.json"))
	return [str(n[1].get("name")) for n in list(filter(lambda o: o[1].get("rarity") == r and str(o[1].get("class")).lower() == p.lower(), ops.items()))]
	

# for i in range(len(data['text'])):
#     x:int = int(data['left'][i])
#     y:int = int(data['top'][i])
#     w:int = int(data['width'][i])
#     h:int = int(data['height'][i])
#     drawBoundingBox(cropped,x,y,w,h,str(data["text"][i]))
# Image.fromarray(bgraToRgba(cropped),"RGBA").show() # type: ignore