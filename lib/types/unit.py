from lib.types.errors import *
from lib.types.misc import * 
from lib.types.skill import * 
from lib.types.cropbox import * 
import cv2
import os
import numpy as np
import re
import difflib
# from PIL import Image
# import pyautogui
import pytesseract # type: ignore
tsr = pytesseract.pytesseract.tesseract_cmd = "./dep/Tesseract-OCR/tesseract.exe"
tess_config = r"--psm 11"
tessOnlyNumbers = r"--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789"
names:list[str] = open("./ref/operatornames.txt").read().split("\n")

class Operator:
	def __init__(self, imagePath:str, profRefData:RefData, promRefData:RefData) -> None:
		self.IMAGE_PATH:str = imagePath
		self.ORIGINAL:cv2.Mat = cv2.imread(self.IMAGE_PATH, cv2.IMREAD_UNCHANGED)
		self.professionAnchor:RefData = profRefData
		self.promotionAnchor:RefData = promRefData
		# crops / positions
		self.prfCropBox:CropBox = CropBox(self.professionAnchor.x, self.professionAnchor.y, self.professionAnchor.size, self.professionAnchor.size, 5)
		self.nameCropBox:CropBox = self.getNamePosition()
		self.rarityCropBox:CropBox = self.getRarityPosition()
		self.levelCropBox:Circle = self.getLevelPosition()
		self.promotionCropBox:CropBox = CropBox(self.promotionAnchor.x, self.promotionAnchor.y, self.promotionAnchor.size, self.promotionAnchor.size, 5)
		self.operatorCropBox:CropBox = self.getOperatorPosition()
		self.potentialCropBox:CropBox = self.getPotentialPosition()
		self.skills:Skills = Skills(self.ORIGINAL.copy(), self.getSkillsPosition())
		# help data for name recognition
		self.profession:str = self.conjectOperatorProfession()
		self.rarityStars:list[tuple[CropBox,int,int,float]] = []
		self.rarity:int = self.conjectOperatorRarity()
		# actual data...
		self.name:str = self.conjectOperatorName(filterNamesByRarityAndProfession(self.rarity, str(self.profession)))
		self.id:str = getIdByName(str(self.name))
		self.level:int = self.conjectOperatorLevel()
		self.promotion:int = self.conjectOperatorPromotionLevel()
		self.potential:int = self.conjectOperatorPotential()
		# self.avatars = 

	def conjectOperatorProfession(self) -> str:
		cropped:cv2.Mat = self.prfCropBox.crop(self.ORIGINAL.copy())
		for c in os.listdir("./ref/classes/alpha/"):
			template:cv2.Mat = toGrayscale(cv2.resize(cv2.imread(f"./ref/classes/mask/{c}"), (self.prfCropBox.w,self.prfCropBox.h)))
			loc:tuple=np.where(cv2.matchTemplate(toGrayscale(cropped), template, cv2.TM_CCOEFF_NORMED)>=0.65) # type: ignore
			if len(loc[0]) > 0:
				return re.findall(r"(?<=class_)\w+", c)[0]
		raise OperatorProfessionConjectionFailed()
	def conjectOperatorName(self, options:list[str]) -> str:
		if 0 < len(options) < 2: return options[0] 
		name:tuple[str,float]|None = conjectTextInRegion(self.ORIGINAL, self.nameCropBox, options, [150, 200, 250, 300, 100, 350, 400, 50])
		if name != None: return name[0]
		raise OperatorNameConjectionFailed(self.IMAGE_PATH)
	def conjectOperatorRarity(self) -> int:
		cropped:cv2.Mat = self.rarityCropBox.crop(self.ORIGINAL.copy())
		mask:cv2.Mat = toGrayscale(cv2.threshold(cropped, 254, 255, cv2.THRESH_BINARY)[1]) # type: ignore / create mask from cropped image
		croppedMasked:cv2.Mat = cv2.bitwise_and(cropped, cropped, mask=mask) # mask the cropped Image
		croppedMaskedGray:cv2.Mat = toGrayscale(croppedMasked)
		stars:list[tuple[int,...]] = []
		for cnt in cv2.findContours(croppedMaskedGray, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]: # type: ignore
			if 50 < cv2.contourArea(cnt) < 400:  # type: ignore / mal gucken
				if len(cnt) < 5: continue
				(x,y), (MA,ma), angle = cv2.fitEllipse(cnt) # type: ignore
				if MA / ma < .5: continue
				stars.append(cnt) # type: ignore
		for star in stars:
			self.rarityStars.append((CropBox(*cv2.boundingRect(star)),x,y,angle)) # type: ignore
		if len(stars) < 1 or len(stars) > 6:
			raise OperatorRarityConjectionFailed(self.IMAGE_PATH)
		return len(stars)
	def conjectOperatorLevel(self) -> int:
		cropped:cv2.Mat = self.levelCropBox.crop(self.ORIGINAL.copy())
		mask:cv2.Mat = toGrayscale(cv2.threshold(cropped, 250, 255, cv2.THRESH_BINARY)[1]) # type: ignore / # tweak thresh if fails
		croppedMasked:cv2.Mat = cv2.bitwise_and(cropped, cropped, mask=mask) # mask the cropped Image
		read:dict[str,list[str]] = pytesseract.image_to_data(toGrayscale(croppedMasked), config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789", output_type=pytesseract.Output.DICT) # type: ignore
		# Image.fromarray(bgraToRgba(croppedMasked)).show()
		filtered = list(filter(lambda n: len(n) > 0, read["text"]))
		if len(filtered) > 0: return int(filtered[0])
		raise OperatorLevelConjectionFailed()
	def conjectOperatorPromotionLevel(self) -> int: # maybe enough confidence without matching multiple sizes 
		data:list[tuple[float,int,int,int]] = [] # (conf, size, x, y)
		streak = 0;
		target:cv2.Mat = toGrayscale(cv2.threshold(self.ORIGINAL.copy(), 225, 255, cv2.THRESH_BINARY)[1]) # type: ignore
		self.promotionCropBox.tolerance = 20
		targetCropped:cv2.Mat = self.promotionCropBox.crop(target)
		for size in range(self.promotionAnchor.size-5,self.promotionAnchor.size+5):
			if len(data) > 0 and streak < 0: break
			for e in os.listdir("./ref/elite/"):
				refImg:cv2.Mat = cv2.imread(f"./ref/elite/{e}", cv2.IMREAD_UNCHANGED)
				refGray:cv2.Mat = toGrayscale(cv2.bitwise_and(refImg, refImg, mask=refImg[:,:,3]))
				refGrayResized:cv2.Mat = cv2.resize(refGray, (size,size))
				res:cv2.Mat = cv2.matchTemplate(targetCropped, refGrayResized, cv2.TM_CCOEFF_NORMED)
				loc:tuple[cv2.Mat, ...] = np.where(res >= .7) # type: ignore
				if len(loc[0]) > 0:
					data.append((float(np.max(res)), int(os.path.splitext(e)[0]))) # type: ignore
					streak = 7
				else: streak-=1
		if len(data) > 0:
			return sorted(data, key=lambda x: -x[0])[0][1]
		raise OperatorPromotionConjectionFailed(self.IMAGE_PATH)
	def conjectOperatorPotential(self) -> int:
		data:list[tuple[float,int,int,int]] = [] # (conf, size, x, y)
		streak = 0;
		self.potentialCropBox.tolerance = 10
		target:cv2.Mat = self.ORIGINAL.copy()
		target = cv2.split(target)[0] # type: ignore / cv2.bitwise_and(target,target,mask=target[:,:,2])
		targetCropped:cv2.Mat = cv2.threshold(self.potentialCropBox.crop(target),230, 255, cv2.THRESH_BINARY)[1] # type: ignore
		for p in os.listdir("./ref/potential/")[::-1]:
			refImg:cv2.Mat = cv2.imread(f"./ref/potential/{p}", cv2.IMREAD_UNCHANGED)
			refImg:cv2.Mat = cv2.threshold(refImg, 230, 255, cv2.THRESH_BINARY)[1] # type: ignore
			refGray:cv2.Mat = cv2.split(refImg)[0] # type: ignore
			refGray = cv2.bitwise_and(refGray,refGray,mask=refImg[:,:,3])
			if len(data) > 0 and streak < 0: break
			for size in range(self.potentialCropBox.h-2,self.potentialCropBox.h+2):
				refGrayResized:cv2.Mat = cv2.resize(refGray, (size, size))
				res:cv2.Mat = cv2.matchTemplate(targetCropped, refGrayResized, cv2.TM_CCOEFF_NORMED)
				loc:tuple[cv2.Mat, ...] = np.where(res >= .83) # type: ignore
				if len(loc[0]) > 0:
					data.append((float(np.max(res)), int(os.path.splitext(p)[0]))) # type: ignore
					streak = 7
				else: streak-=1
		if len(data) > 0:
			return sorted(data, key=lambda x: -x[0])[0][1]
		raise OperatorPotentialConjectionFailed(self.IMAGE_PATH)

	def getNamePosition(self) -> CropBox:
		return CropBox(
			x=int(self.professionAnchor.x),
			y=int(self.professionAnchor.y-1.5*self.professionAnchor.size),
			w=int(7*self.professionAnchor.size),
			h=int(1.5*self.professionAnchor.size),
			tolerance=5
		)
	def getRarityPosition(self) -> CropBox:
		return CropBox(
			x=int(self.professionAnchor.x),
			y=int(self.professionAnchor.y-1.85*self.professionAnchor.size),
			w=int(1.7*self.professionAnchor.size),
			h=int(.28*self.professionAnchor.size),
			tolerance=5
		)
	def getLevelPosition(self) -> Circle:
		# gray_blur = cv2.GaussianBlur(gray, (7, 7), 0)
		circles:cv2.Mat|None = cv2.HoughCircles(toGrayscale(self.ORIGINAL.copy()), cv2.HOUGH_GRADIENT, 1, 100, param1=255, param2=100, minRadius=int(self.professionAnchor.size/2), maxRadius=self.professionAnchor.size) # type: ignore
		# if circles is not None:
		return Circle(*np.round(circles[0,])[0]) # type: ignore
	def getOperatorPosition(self) -> CropBox:
		return CropBox(
			x=int(self.professionAnchor.x+4*self.professionAnchor.size),
			y=int(self.professionAnchor.y-6.2*self.professionAnchor.size),
			w=int(self.professionAnchor.size*5),
			h=int(self.professionAnchor.size*6.5)
		)
	def getPotentialPosition(self) -> CropBox:
		return CropBox(
			x=int(self.promotionAnchor.x+1.95*self.promotionAnchor.size),
			y=int(self.promotionAnchor.y),
			w=int(self.promotionAnchor.size),
			h=int(1*self.promotionAnchor.size),
			tolerance=5
		)	
	def getSkillsPosition(self) -> SkillBox:
		return SkillBox(
			x=int(self.promotionAnchor.x*1),
			y=int(self.promotionAnchor.y*1.52),
			w=int(self.promotionAnchor.size*3.81),
			h=int(self.promotionAnchor.size*.77),
			tolerance=10
		)

	def drawAllBounds(self) -> cv2.Mat:
		cpy:cv2.Mat = self.ORIGINAL.copy()
		drawBoundingBox(cpy, *self.prfCropBox.toTuple(), text=self.profession)
		starPos:list[tuple[int,...]] = [s[0].add([self.rarityCropBox.toTuple()]) for s in self.rarityStars]
		for p in range(len(starPos)):
			drawBoundingBox(cpy, *starPos[p], text=str(p))
		drawBoundingBox(cpy, *self.nameCropBox.toTuple(), text=self.id, inset=True)
		drawBoundingBox(cpy, *self.levelCropBox.getBoundingBox().toTuple(), text=f"LVL {self.level}")
		drawBoundingBox(cpy, *self.promotionCropBox.toTuple(), text=f"E {self.promotion}", inset=True)
		drawBoundingBox(cpy, *self.potentialCropBox.toTuple(), text=f"POT {self.potential}")
		return cpy


def getProfessionReferenceData(original:cv2.Mat) -> RefData:
	data:list[tuple[float,int,int,int]] = [] # (conf, size, x, y)
	streak = 0;
	target:cv2.Mat = toGrayscale(original.copy())
	for size in range(108,150,1):
		if len(data) > 0 and streak < 0: break
		for c in os.listdir("./ref/classes/alpha/"):
			template:cv2.Mat = cv2.imread(f"./ref/classes/alpha/{c}")
			templateResized:cv2.Mat = cv2.resize(template, (size,size))
			templateResizedGray:cv2.Mat = toGrayscale(templateResized)
			res:cv2.Mat = cv2.matchTemplate(target, templateResizedGray, cv2.TM_CCOEFF_NORMED)
			loc:tuple=np.where(res>=0.8) # type: ignore
			if len(loc[0]) > 0:
				data.append((float(np.max(res)), size, loc[1][0], loc[0][0])) # type: ignore
				streak = 7
			else: streak-=1
	return RefData(*sorted(data, key=lambda x: -x[0])[0])
def getPromotionReferenceData(original:cv2.Mat) -> RefData:
	data:list[tuple[float,int,int,int]] = [] # (conf, size, x, y)
	streak = 0;
	target:cv2.Mat = toGrayscale(cv2.threshold(original.copy(), 225, 255, cv2.THRESH_BINARY)[1]) # type: ignore
	for size in range(100,140):
		if len(data) > 0 and streak < 0: break
		for e in os.listdir("./ref/elite/"):
			refImg:cv2.Mat = cv2.imread(f"./ref/elite/{e}", cv2.IMREAD_UNCHANGED)
			refGray:cv2.Mat = toGrayscale(cv2.bitwise_and(refImg, refImg, mask=refImg[:,:,3]))
			refGrayResized:cv2.Mat = cv2.resize(refGray, (size,size))
			res:cv2.Mat = cv2.matchTemplate(target, refGrayResized, cv2.TM_CCOEFF_NORMED)
			loc:tuple[cv2.Mat, ...] = np.where(res >= .7) # type: ignore
			if len(loc[0]) > 0:
				data.append((float(np.max(res)),size,loc[1][0],loc[0][0])) # type: ignore
				streak = 7
			else: streak-=1
	return RefData(*sorted(data, key=lambda x: -x[0])[0])

def conjectTextInRegionChunked(original:cv2.Mat, region:CropBox, options:list[str], chunkSize:int) -> list[tuple[str,float]]:
	all:list[tuple[str,float]] = []
	for cropped in region.cropSplit(original.copy(), chunkSize):
		mask:cv2.Mat = toGrayscale(cv2.threshold(cropped, 254, 255, cv2.THRESH_BINARY)[1]) # type: ignore / create mask from cropped image
		kernel:cv2.Mat = cv2.getStructuringElement(cv2.MORPH_RECT, (int(mask.shape[0]/10),int(mask.shape[1]/10))) # type: ignore
		mask2:cv2.Mat = cv2.bitwise_not(cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)) # type: ignore
		croppedMasked:cv2.Mat = cv2.bitwise_and(cropped, cropped, mask=cv2.bitwise_and(mask,mask2)) # mask the cropped Image
		read:dict[str,list[str]] = pytesseract.image_to_data(toGrayscale(croppedMasked), config=tess_config, output_type=pytesseract.Output.DICT) # type: ignore
		filteredData = list(filter(lambda x: len(str(x)) > 2, read["text"]))
		matches1:list[str] = difflib.get_close_matches("".join([f.capitalize() for f in filteredData]), options, n=1000, cutoff=.58)
		if len(matches1) > 0:
			simScore:float = difflib.SequenceMatcher(None, "".join([f.capitalize() for f in filteredData]), matches1[0]).ratio()
			all.append((matches1[0], simScore))
	return all
def conjectTextInRegion(original:cv2.Mat, region:CropBox, options:list[str], chunkSizees:list[int]=[150, 300]) -> tuple[str,float]|None:
	cropped:cv2.Mat = region.crop(original.copy())
	mask:cv2.Mat = toGrayscale(cv2.threshold(cropped, 254, 255, cv2.THRESH_BINARY)[1]) # type: ignore / create mask from cropped image
	kernel:cv2.Mat = cv2.getStructuringElement(cv2.MORPH_RECT, (int(mask.shape[0]/10),int(mask.shape[1]/10))) # type: ignore
	mask2:cv2.Mat = cv2.bitwise_not(cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)) # type: ignore
	croppedMasked:cv2.Mat = cv2.bitwise_and(cropped, cropped, mask=cv2.bitwise_and(mask,mask2)) # mask the cropped Image
	read:dict[str,list[str]] = pytesseract.image_to_data(toGrayscale(croppedMasked), config=tess_config, output_type=pytesseract.Output.DICT) # type: ignore
	# print(read["text"])
	filteredData = list(filter(lambda x: len(str(x)) > 2, read["text"]))
	matches1:list[str] = difflib.get_close_matches("".join([f.capitalize() for f in filteredData]), options, n=1000, cutoff=.58)
	if len(matches1) > 0:
		simScore:float = difflib.SequenceMatcher(None, "".join([f.capitalize() for f in filteredData]), matches1[0]).ratio()
		return (matches1[0], simScore)
	else:
		for cs in chunkSizees:
			res:list[tuple[str, float]] = conjectTextInRegionChunked(original, region, options, cs)
			if len(res) > 0:
				return res[0]
		return None
