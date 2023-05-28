import os
import json
from datetime import datetime as dt
from lib.types.errors import *
import cv2
from lib.types.cropbox import *

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
		cv2.putText(image, text, (x if not inset else x+5, (y - 10) if not inset else (y + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2) # type: ignore
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
	ops:list[dict[str, str]] = dict(json.load(open("./ref/class2op.json"))).get(c, [])
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
	


class Delta():
	def __init__(self, time:dt, description:str|None=None) -> None:
		self.TIME:dt = time
		self.description:str|None = description

class TimeTracker():
	def __init__(self, startTime:dt) -> None:
		self.START_TIME:dt = startTime
		self.deltas:list[Delta] = []

	def add(self, d:Delta) -> None:
		self.deltas.append(d)

	def diff(self) -> list[tuple[str|None, float]]:
		return [(self.deltas[d].description, (self.deltas[d].TIME - self.START_TIME if d == 0 else self.deltas[d].TIME - self.deltas[d-1].TIME).total_seconds()) for d in range(len(self.deltas))]

# for i in range(len(data['text'])):
#     x:int = int(data['left'][i])
#     y:int = int(data['top'][i])
#     w:int = int(data['width'][i])
#     h:int = int(data['height'][i])
#     drawBoundingBox(cropped,x,y,w,h,str(data["text"][i]))
# Image.fromarray(bgraToRgba(cropped),"RGBA").show() # type: ignore

def findLetters(cropped:cv2.Mat, minArea:int=0, maxArea:int=10000) -> list[CropBox]:
	gray:cv2.Mat = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
	edges:cv2.Mat = cv2.Canny(gray, 10, 0)#type:ignore
	contours:cv2.Mat = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] # type: ignore
	cropBoxes:list[CropBox] = []
	for cnt in contours:
		if not minArea < cv2.contourArea(cnt) < maxArea: continue # type: ignore
		cropBoxes.append(CropBox(*cv2.boundingRect(cnt), tolerance=0)) # type: ignore
	return cropBoxes