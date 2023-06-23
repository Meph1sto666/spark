import os
import json
from datetime import datetime as dt
import colorama
from lib.types.errors import *
import cv2
from lib.types.cropbox import *		

class RefData:
	"""Reference data class for orientation of OCR

	Attributes
		conf (float): Confidence for matched image
		size (int): Size of the matched image (square)
		x (int): x location
		y (int): y location
	"""
	def __init__(self, conf:float, size:int, x:int, y:int) -> None:
		self.conf: float = conf
		self.size: int = size
		self.x: int = x
		self.y: int = y
	def toTuple(self) -> tuple[float, int, int, int]:
		"""Converts the object into a tuple

		Returns:
			tuple[float, int, int, int]: (confidence, size, x, y)
		"""
		return (self.conf, self.size, self.x, self.y)

def drawBoundingBox(image:cv2.Mat,x:int,y:int,w:int,h:int,text:str|None=None, inset:bool=False) -> cv2.Mat:
	"""Draws a bounding box in an image

	Args:
		image (cv2.Mat): Image to draw on
		x (int): x pos
		y (int): y pos
		w (int): Rectangle width
		h (int): Rectangle height
		text (str | None, optional): Text to write to the rect. Defaults to None.
		inset (bool, optional): If true the text will be inside the rectangle else outside. Defaults to False.

	Returns:
		cv2.Mat: Image with drawn boxes
	"""
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) # type: ignore
	if text != None:
		cv2.putText(image, text, (x if not inset else x+5, (y - 10) if not inset else (y + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2) # type: ignore
	return image
def bgraToRgba(img:cv2.Mat) -> cv2.Mat:
	"""Converts an image from BGRA to RGBA

	Args:
		img (cv2.Mat): Image to convert

	Returns:
		cv2.Mat: Converted image
	"""
	return cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
def rgbaToBgra(img:cv2.Mat) -> cv2.Mat:
	"""Converts an image from RGBA to BGRA

	Args:
		img (cv2.Mat): Image to convert

	Returns:
		cv2.Mat: Converted image
	"""
	return cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
def toGrayscale(image:cv2.Mat) -> cv2.Mat:
	"""Converts an image from to grayscale

	Args:
		img (cv2.Mat): Image to convert

	Returns:
		cv2.Mat: Converted image
	"""
	return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def filterNamesByProfession(c:str) -> list[str]:
	"""Filters the names from class2op.json by their operator class

	Args:
		c (str): class/profession

	Returns:
		list[str]: all operator names with profession
	"""
	ops:list[dict[str, str]] = dict(json.load(open("./ref/class2op.json"))).get(c, [])
	return [o["name"] for o in ops]
def filterAvatarsById(id:str) -> list[str]:
	"""Filters the avatars from ./ref/avatars/ by the operators id

	Args:
		id (str): id

	Returns:
		list[str]: All filenames of operators with id
	"""
	# ops:list[dict[str, str]] = dict(json.load(open("./ref/class2op.json"))).get(c, [])
	# opIds:list[str] = [o.get("id", "None").split("_")[1] for o in ops]
	return list(filter(lambda x: id in x, os.listdir("./ref/avatars/")))
def getIdByName(name:str) -> str:
	"""Finds the operator id by its name

	Args:
		name (str): Operator name

	Raises:
		OperatorNameNotFound: When the operator name is not found

	Returns:
		str: Operatior id
	"""
	ops:dict[str,dict[str,str]] = json.load(open("./ref/operators.json"))
	id:str|None = list(filter(lambda o: o[1].get("name")==name, ops.items()))[0][1].get("id", None)
	if id == None:
		raise OperatorNameNotFound()
	return id
def getSkinsById(id:str) -> list[str]:
	"""Finds all avatar files of the operator by its id

	Args:
		id (str): operator id

	Returns:
		list[str]: Filenames of the operator skins
	"""
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

	def diff(self) -> dict[str|None, float]:#list[tuple[str|None, float]]:
		# return [(self.deltas[d].description, (self.deltas[d].TIME - self.START_TIME if d == 0 else self.deltas[d].TIME - self.deltas[d-1].TIME).total_seconds()) for d in range(len(self.deltas))]
		return dict([(self.deltas[d].description, (self.deltas[d].TIME - self.START_TIME if d == 0 else self.deltas[d].TIME - self.deltas[d-1].TIME).total_seconds()) for d in range(len(self.deltas))])

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

def timeToColor(t:float) -> str:
	"""Converts the time to a colorama string for easier speed recognition on console output (0-1000ms)

	Args:
		t (float): Taken time

	Returns:
		str: Corresponding color string
	"""
	c:str = colorama.Fore.RESET
	if   t < .1: c = colorama.Fore.WHITE
	elif t < .2: c = colorama.Fore.LIGHTMAGENTA_EX
	elif t < .3: c = colorama.Fore.MAGENTA
	elif t < .4: c = colorama.Fore.LIGHTCYAN_EX
	elif t < .5: c = colorama.Fore.CYAN
	elif t < .6: c = colorama.Fore.LIGHTGREEN_EX
	elif t < .7: c = colorama.Fore.GREEN
	elif t < .8: c = colorama.Fore.LIGHTYELLOW_EX
	elif t < .9: c = colorama.Fore.YELLOW
	elif t < 1.: c = colorama.Fore.LIGHTRED_EX
	else: c = colorama.Fore.RED
	return c

def timeToColorPrec(t:float) -> str:
	"""Converts the time to a colorama string for easier speed recognition on console output (more precise; 0-500ms)

	Args:
		t (float): Taken time

	Returns:
		str: Corresponding color string
	"""
	c:str = colorama.Fore.RESET
	if   t < .050: c = colorama.Fore.WHITE
	elif t < .100: c = colorama.Fore.LIGHTMAGENTA_EX
	elif t < .150: c = colorama.Fore.MAGENTA
	elif t < .200: c = colorama.Fore.LIGHTCYAN_EX
	elif t < .250: c = colorama.Fore.CYAN
	elif t < .300: c = colorama.Fore.LIGHTGREEN_EX
	elif t < .350: c = colorama.Fore.GREEN
	elif t < .400: c = colorama.Fore.LIGHTYELLOW_EX
	elif t < .450: c = colorama.Fore.YELLOW
	elif t < .500: c = colorama.Fore.LIGHTRED_EX
	else: c = colorama.Fore.RED
	return c