from typing import * # type: ignore

from lib.types.errors import *
from lib.types.misc import * 
from lib.types.skill import * 
from lib.types.cropbox import * 
from lib.types.module import * 
import cv2
import os
import numpy as np
import re
import difflib
import gzip
import pickle
from datetime import datetime as dt
# from PIL import Image
# import pyautogui
import pytesseract # type: ignore
tsr = pytesseract.pytesseract.tesseract_cmd = "./dep/Tesseract-OCR/tesseract.exe"
tess_config = r"--psm 11"
tessOnlyNumbers = r"--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789"
names:list[str] = open("./ref/operatornames.txt","r").read().split("\n")

class Operator:
	"""Representation of an Arknights operator with all important meta data
 
		Attributes:
			IMAGE_PATH (str): Path to target image
			original (cv2.Mat): Image as np array (BGRA)
			imginf (tuple[np.dtype[np.generic], Tuple[int, ...]]): Numpy array data (dtype, shape)
			
			professionAnchor (RefData): Profession/Operator class reference data
			promotionAnchor (RefData): Promotion reference data
			tTracker (TimeTracker): Speed measurment
			
			prfCropBox (CropBox): Cropbox for operator class
			nameCropBox (CropBox): Cropbox for operator name
			rarityCropBox (CropBox): Cropbox for operator rarity
			levelCropBox (CropBox): Cropbox for operator level
			promotionCropBox (CropBox): Cropbox for operator promotion level
			potentialCropBox (CropBox): Cropbox for operator potential
			moduleTypeCropBox (CropBox): Cropbox for operator module type
			moduleStageCropBox (CropBox): Cropbox for operator module stage
			favouriteCropBox (CropBox): Cropbox for operator favourite selector

			
	"""
	def __init__(self, imagePath:str, profRefData:RefData, promRefData:RefData) -> None:
		"""_summary_

		Args:
			imagePath (str): _description_
			profRefData (RefData): _description_
			promRefData (RefData): _description_
		"""
		self.IMAGE_PATH:str = imagePath
		self.original:cv2.Mat = cv2.imread(self.IMAGE_PATH, cv2.IMREAD_UNCHANGED)
		self.imgInf:tuple[np.dtype[np.generic], Tuple[int, ...]] = (self.original.dtype, self.original.shape)
		self.professionAnchor:RefData = profRefData
		self.promotionAnchor:RefData = promRefData
		# ===crops / positions===
		self.tTracker:TimeTracker = TimeTracker(dt.now())
		self.prfCropBox:CropBox = CropBox(self.professionAnchor.x, self.professionAnchor.y, self.professionAnchor.size, self.professionAnchor.size, 5)
		self.nameCropBox:CropBox = self.getNamePosition()
		self.rarityCropBox:CropBox = self.getRarityPosition()
		self.levelCropBox:CropBox = self.getLevelPosition()
		self.promotionCropBox:CropBox = CropBox(self.promotionAnchor.x, self.promotionAnchor.y, self.promotionAnchor.size, self.promotionAnchor.size, 5)
		# self.operatorCropBox:CropBox = self.getOperatorPosition()
		self.potentialCropBox:CropBox = self.getPotentialPosition()
		self.moduleTypeCropBox:CropBox = self.getModuleTypePosition()
		self.moduleStageCropBox:CropBox = self.getModuleStagePosition()
		self.favouriteCropBox:CropBox = self.getFavouritePosition()
		self.tTracker.add(Delta(dt.now(), "cropBoxes"))
		# print(self.nameCropBox, self.imgInf, self.professionAnchor.x)
		# Image.fromarray(self.levelCropBox.crop(self.original)).show()


		# ===help data for name recognition===
		self.profession:str = self.conjectOperatorProfession()
		self.tTracker.add(Delta(dt.now(), "prof"))
		self.rarityStars:list[tuple[CropBox,int,int,float]] = []
		self.rarity:int = self.conjectOperatorRarity()
		self.tTracker.add(Delta(dt.now(), "rarity"))
		
		# ===actual data...===
		self.name:str = self.conjectOperatorName(filterNamesByRarityAndProfession(self.rarity, str(self.profession)))
		self.tTracker.add(Delta(dt.now(), "name"))
		self.id:str = getIdByName(str(self.name))
		self.tTracker.add(Delta(dt.now(), "id"))
		self.level:int = self.conjectOperatorLevel()
		self.tTracker.add(Delta(dt.now(), "level"))
		self.promotion:int = self.conjectOperatorPromotionLevel()
		self.tTracker.add(Delta(dt.now(), "prom"))
		self.potential:int = self.conjectOperatorPotential()
		self.tTracker.add(Delta(dt.now(), "pot"))
		self.skills:Skills = Skills(self.original, self.promotionAnchor, self.rarity)
		self.tTracker.add(Delta(dt.now(), "skills"))
		self.module:Module = Module(self.original, self.id, self.promotion, self.moduleStageCropBox, self.moduleTypeCropBox)
		self.tTracker.add(Delta(dt.now(), "module"))
		self.loved:bool = self.conjectFavouriteStatus()
		self.tTracker.add(Delta(dt.now(), "fav"))
		self.avatar:str|None = None
		# print(self.tTracker.diff())

	def conjectOperatorProfession(self) -> str:
		cropped:cv2.Mat = self.prfCropBox.crop(self.original)
		for c in os.listdir("./ref/classes/alpha/"):
			template:cv2.Mat = toGrayscale(cv2.resize(cv2.imread(f"./ref/classes/mask/{c}"), (self.prfCropBox.w,self.prfCropBox.h)))
			loc:tuple=np.where(cv2.matchTemplate(toGrayscale(cropped), template, cv2.TM_CCOEFF_NORMED)>=0.65) # type: ignore
			if len(loc[0]) > 0: return re.findall(r"(?<=class_)\w+", c)[0] # type: ignore
		raise OperatorProfessionConjectionFailed(self.IMAGE_PATH)
	def conjectOperatorName(self, options:list[str]) -> str:
		if 0 < len(options) < 2: return options[0]
		name:tuple[str,float]|None = conjectTextInRegion(self.original, self.nameCropBox, options, [150, 200, 250, 300, 100, 350, 400, 50])
		if name != None: return name[0]
		raise OperatorNameConjectionFailed(self.IMAGE_PATH)
	def conjectOperatorRarity(self) -> int:
		cropped:cv2.Mat = self.rarityCropBox.crop(self.original)
		gray:cv2.Mat = toGrayscale(cropped)
		thresh:cv2.Mat = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)[1] # type: ignore
		croppedArea:int = cropped.shape[0]*cropped.shape[1]
		labels, stats = cv2.connectedComponentsWithStats(thresh)[1:3]
		for label in range(1, labels.max()):
			area:int = stats[label,cv2.CC_STAT_AREA]
			if area < croppedArea*.01 or area > croppedArea*.05: labels[labels==label] = 0
		threshed:cv2.Mat = cv2.bitwise_and(gray, gray, mask=(labels>0).astype(np.uint8))
		# Image.fromarray(threshed).save(f"./preprocessed/{os.path.split(os.path.splitext(self.IMAGE_PATH)[0])[-1]}.png") # type: ignore
		stars:list[tuple[int,...]] = []
		for cnt in cv2.findContours(threshed, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]: # type: ignore
			if croppedArea*.01 < cv2.contourArea(cnt) < croppedArea*.1:  # type: ignore / mal gucken
				if len(cnt) < 5: continue
				(x,y), (MA,ma), angle = cv2.fitEllipse(cnt) # type: ignore
				if MA / ma < .5: continue
				stars.append(cnt) # type: ignore
		for star in stars:
			self.rarityStars.append((CropBox(*cv2.boundingRect(star)),x,y,angle)) # type: ignore
		if 0 < len(stars) < 7:
			# print(len(stars))
			return len(stars)
		raise OperatorRarityConjectionFailed(self.IMAGE_PATH)
	def conjectOperatorLevel(self) -> int:
		cropped:cv2.Mat = self.levelCropBox.crop(self.original)
		gray:cv2.Mat = toGrayscale(cropped)
		croppedArea:int = gray.shape[0]*gray.shape[1]
		thresh:cv2.Mat = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1] # type: ignore
		labels, stats = cv2.connectedComponentsWithStats(thresh)[1:3]
		for label in range(1, labels.max()):
			area:int = stats[label,cv2.CC_STAT_AREA]
			if area < croppedArea*.05: labels[labels==label] = 0
		threshed:cv2.Mat = cv2.bitwise_and(gray, gray, mask=(labels>0).astype(np.uint8))
		threshed = cv2.GaussianBlur(threshed, (5,5), 10) # type: ignore
		# Image.fromarray(threshed).save(f"./preprocessed/preprocess_{self.name}.png","png")
		read:dict[str,list[str]] = pytesseract.image_to_data(cv2.bitwise_not(threshed), config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789", output_type=pytesseract.Output.DICT) # type: ignore
		filtered:list[str] = []
		for r in read["text"]:
			if len(r) > 0: filtered.append(r)
		if len(filtered) > 0: return int(filtered[0])
		raise OperatorLevelConjectionFailed(self.IMAGE_PATH)

	def conjectOperatorPromotionLevel(self) -> int:
		target:cv2.Mat = toGrayscale(cv2.threshold(self.original, 254, 255, cv2.THRESH_BINARY)[1]) # type: ignore
		cropped:cv2.Mat = self.promotionCropBox.crop(target)
		cArea:int = cropped.shape[0]*cropped.shape[1]
		promotionsPxs:list[float] = [.03*cArea, .081*cArea, .135*cArea]
		for pxi in range(len(promotionsPxs)):
			if np.count_nonzero(cropped) < promotionsPxs[pxi]: return pxi # type: ignore
		raise OperatorPromotionConjectionFailed(self.IMAGE_PATH)
	def conjectOperatorPotential(self) -> int:
		target:cv2.Mat = self.potentialCropBox.crop(self.original)
		targetCropped:cv2.Mat = cv2.threshold(cv2.split(target)[0], 230, 255, cv2.THRESH_BINARY)[1] # type: ignore
		cArea:int = targetCropped.shape[0]*targetCropped.shape[1]
		potPxlThreshs:list[int] = [int(.025*cArea), int(.045*cArea), int(.065*cArea), int(.08*cArea), int(.095*cArea), int(.15*cArea)] # 1000, 2000, 3000
		" p6 = 4659, p5 = 3770, p4 = 3209, p3 = 2561, p2 = 1812, p1 = 934 "
		for pti in range(len(potPxlThreshs)):
			if np.count_nonzero(targetCropped) < potPxlThreshs[pti]: # type: ignore
				return pti+1
		raise OperatorPotentialConjectionFailed(self.IMAGE_PATH)

	def conjectFavouriteStatus(self) -> bool:
		cropped:cv2.Mat = self.favouriteCropBox.crop(self.original)
		bgr:tuple[cv2.Mat,...] = cv2.split(cropped) # type: ignore
		yellowMask:cv2.Mat = cv2.bitwise_and(bgr[1],bgr[2])
		yellowMask:cv2.Mat = cv2.bitwise_xor(yellowMask, bgr[0])
		yellowMask = cv2.threshold(yellowMask, 100, 255, cv2.THRESH_BINARY)[1] # type: ignore
		return bool(np.sum(yellowMask==255) > 350) # type: ignore

	def getNamePosition(self) -> CropBox:
		return CropBox(
			x=int(self.professionAnchor.size*.2),
			# y=int(self.professionAnchor.size*5.5+(self.original.shape[0]-self.original.shape[1]/(16/9))/2),
			y=int((self.professionAnchor.y+max(0,(self.original.shape[0]-self.original.shape[1]/(16/9))/4))*.8),
			w=int(self.professionAnchor.size*5), # 5.8 <- 7
			h=int(self.professionAnchor.size*1.2),
			tolerance=min(10, int(self.professionAnchor.size*.2))
		)
	def getRarityPosition(self) -> CropBox:
		return CropBox(
			x=int(self.professionAnchor.x*1),
			y=int((self.professionAnchor.y+max(0,(self.original.shape[0]-self.original.shape[1]/(16/9))/4))*.73), # fails on >16:9
			w=int(self.professionAnchor.size*1.7),
			h=int(self.professionAnchor.size*.28),
			tolerance=5
		)
	def getLevelPosition(self) -> CropBox:
		return CropBox(
			x=int(self.promotionAnchor.x+self.promotionAnchor.size*0.05),
			y=int((self.promotionAnchor.y+(self.original.shape[0]-self.original.shape[1]/(16/9))/2)*.5),
			w=int(self.promotionAnchor.size),
			h=int(self.promotionAnchor.size*.75)
		)

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
			w=int(self.promotionAnchor.size*1.1),
			h=int(self.promotionAnchor.size*1.1),
			tolerance=20
		)	
	# def getSkillsPosition(self) -> SkillBox:
	# 	return SkillBox(
	# 		x=int(self.promotionAnchor.x*1),
	# 		y=int(self.promotionAnchor.y*1.52),
	# 		w=int(self.promotionAnchor.size*3.81),
	# 		h=int(self.promotionAnchor.size*.77),
	# 		tolerance=10
	# 	)
	def getModuleTypePosition(self) -> CropBox:
		return CropBox(
			x=int(self.promotionAnchor.x*1.21),
			y=int(self.promotionAnchor.y*2.23),
			w=int(self.promotionAnchor.size*1),
			h=int(self.promotionAnchor.size*1),
			tolerance=70
		)
	def getModuleStagePosition(self) -> CropBox:
		return CropBox(
			x=int(self.professionAnchor.size*14),
			y=int(self.professionAnchor.size*6),
			w=int(self.professionAnchor.size*.5),
			h=int(self.professionAnchor.size*.5),
			tolerance=70
		)
	def getFavouritePosition(self) -> CropBox:
		return CropBox(
			x=int(self.professionAnchor.size*8.68),
			y=int(self.professionAnchor.size*.1+(self.original.shape[0]-self.original.shape[1]/(16/9))/2),
			w=int(self.professionAnchor.size*.75),
			h=int(self.professionAnchor.size*.75),
			tolerance=0
		)

	def drawAllBounds(self) -> cv2.Mat:
		cpy:cv2.Mat = self.original
		drawBoundingBox(cpy, *self.prfCropBox.toTuple(), text=self.profession)
		starPos:list[tuple[int,...]] = [s[0].add([self.rarityCropBox.toTuple()]) for s in self.rarityStars]
		for p in range(len(starPos)):
			drawBoundingBox(cpy, *starPos[p], text=str(p))
		drawBoundingBox(cpy, *self.nameCropBox.toTuple(), text=self.id, inset=True)
		drawBoundingBox(cpy, *self.levelCropBox.toTuple(), text=f"LVL {self.level}")
		drawBoundingBox(cpy, *self.promotionCropBox.toTuple(), text=f"E {self.promotion}", inset=True)
		drawBoundingBox(cpy, *self.potentialCropBox.toTuple(), text=f"POT {self.potential}")
		drawBoundingBox(cpy, *self.skills.sb.toTuple(), text=f"R {self.skills.rank}")
		for m in self.skills.masteries:
			if m==None: continue
			if m.masteryCropBox==None: continue
			drawBoundingBox(cpy, *m.masteryCropBox.add([m.skillCropBox.toTuple()]), text=f"M {m.mastery}")
		if self.module.foundTypeCropBox != None:
			drawBoundingBox(cpy, *self.module.foundTypeCropBox.toTuple(), text=f"M{self.module.type} S{self.module.stage}")
		return cpy

	def save(self, folder:str) -> None:
		# del self.original
		self.original = gzip.compress(self.original.tobytes()) # type: ignore
		pickle.dump(self, open((folder + "/" if not folder.endswith("/") else folder) + self.id + ".spec", "wb"),protocol=pickle.HIGHEST_PROTOCOL)
		# self.recreateImg()
	def recreateImg(self) -> None:
		self.original = np.frombuffer(gzip.decompress(self.original), dtype=self.imgInf[0]).reshape(self.imgInf[1]) # type: ignore

	def toJson(self) -> dict[str, str | None | int | list[int] | dict[str, str | int | None]]:
		data:dict[str, str | None | int | list[int] | dict[str, str | int | None]] = {
			"id": self.id,
			"level": self.level,
			"elite": self.promotion,
			"potential": self.potential,
			"skill_level": self.skills.rank,
			"masteries": [m.mastery if m!=None else -1 for m in self.skills.masteries] if self.skills.isMasteryable() else [],
			"module": None,
			"loved": self.loved,
			"skin": self.avatar
		}
		if self.module.type != None:
			data["module"] = {
				"type": self.module.type.lower(),
				"stage": self.module.stage
			}
		return data

def getProfessionReferenceData(originalPath:str, startSize:int, endSize:int, callback:Callable[..., Any]|None=None) -> RefData:
	"""Creates profession reference data for an image

	Args:
		originalPath (str): Target image
		startSize (int): Reference image size to start with
		endSize (int): Reference image size to end with
		callback (Callable[..., Any] | None, optional): callback function for progress logging. Defaults to None.

	Returns:
		RefData: Found reference data
	"""
	data:list[tuple[float,int,int,int]] = [] # (conf, size, x, y)
	streak = 0;
	target:cv2.Mat = toGrayscale(cv2.imread(originalPath, cv2.IMREAD_UNCHANGED))
	refList:list[str] = os.listdir("./ref/classes/alpha/")
	inc:int = 0
	for size in range(startSize, endSize):
		if callback != None:
			callback((inc/((endSize-startSize)*len(refList)))*100)
		for c in refList:
			if len(data) > 0 and streak < 0: break
			template:cv2.Mat = cv2.imread(f"./ref/classes/alpha/{c}")
			templateResized:cv2.Mat = cv2.resize(template, (size,size))
			templateResizedGray:cv2.Mat = toGrayscale(templateResized)
			res:cv2.Mat = cv2.matchTemplate(target, templateResizedGray, cv2.TM_CCOEFF_NORMED)
			loc:tuple=np.where(res>=0.8) # type: ignore
			if len(loc[0]) > 0:
				data.append((float(np.max(res)), size, loc[1][0], loc[0][0])) # type: ignore
				streak = 7
			else: streak-=1
			inc+=1
	return RefData(*sorted(data, key=lambda x: -x[0])[0])

def getPromotionReferenceData(originalPath:str, startSize:int, endSize:int, callback:Callable[..., Any]|None=None) -> RefData:
	"""Creates promotion reference data for an image

	Args:
		originalPath (str): Path to target image
		startSize (int): Reference image size to start with
		endSize (int): Reference image size to end with
		callback (Callable[..., Any] | None, optional): callback function for progress logging. Defaults to None.

	Returns:
		RefData: Found reference data
	"""
	data:list[tuple[float,int,int,int]] = [] # (conf, size, x, y)
	streak = 0;
	target:cv2.Mat = toGrayscale(cv2.threshold(cv2.imread(originalPath, cv2.IMREAD_UNCHANGED), 225, 255, cv2.THRESH_BINARY)[1]) # type: ignore
	refList:list[str] = os.listdir("./ref/elite/")
	inc:int = 0
	for size in range(startSize, endSize):
		if callback != None:
			callback((inc/((endSize-startSize)*len(refList)))*100)
		for e in refList:
			if len(data) > 0 and streak < 0: break
			refImg:cv2.Mat = cv2.imread(f"./ref/elite/{e}", cv2.IMREAD_UNCHANGED)
			refGray:cv2.Mat = toGrayscale(cv2.bitwise_and(refImg, refImg, mask=refImg[:,:,3]))
			refGrayResized:cv2.Mat = cv2.resize(refGray, (size,size))
			res:cv2.Mat = cv2.matchTemplate(target, refGrayResized, cv2.TM_CCOEFF_NORMED)
			loc:tuple[cv2.Mat, ...] = np.where(res >= .7) # type: ignore
			if len(loc[0]) > 0:
				data.append((float(np.max(res)),size,loc[1][0],loc[0][0])) # type: ignore
				streak = 7
			else: streak-=1
			inc+=1
	return RefData(*sorted(data, key=lambda x: -x[0])[0])

def conjectTextInRegionChunked(original:cv2.Mat, region:CropBox, options:list[str], chunkSize:int) -> list[tuple[str,float]]:
	"""Reads the text in given reagion with tesseract by creating smaller chunks from the original image and compares found results to a list of valid options

	Args:
		original (cv2.Mat): Target image
		region (CropBox): Region to read from
		options (list[str]): Valid options
		chunkSizes (int): Chunk sizes for cropping..

	Returns:
		tuple[str,float]: The found text (text, confidence);
	"""
	all:list[tuple[str,float]] = []
	for cropped in region.cropSplit(original, chunkSize):
		mask:cv2.Mat = toGrayscale(cv2.threshold(cropped, 254, 255, cv2.THRESH_BINARY)[1]) # type: ignore / create mask from cropped image
		kernel:cv2.Mat = cv2.getStructuringElement(cv2.MORPH_RECT, (int(mask.shape[0]/6),int(mask.shape[1]/10))) # type: ignore
		mask2:cv2.Mat = cv2.bitwise_not(cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)) # type: ignore
		croppedMasked:cv2.Mat = cv2.bitwise_and(cropped, cropped, mask=cv2.bitwise_and(mask,mask2)) # mask the cropped Image
		read:dict[str,list[str]] = pytesseract.image_to_data(toGrayscale(croppedMasked), config=tess_config, output_type=pytesseract.Output.DICT) # type: ignore
		filteredData:list[str] = []
		for r in read["text"]:
			if len(r) > 2: filteredData.append(r)
		matches1:list[str] = difflib.get_close_matches("".join([f.capitalize() for f in filteredData]), options, n=1000, cutoff=.5)
		if len(matches1) > 0:
			simScore:float = difflib.SequenceMatcher(None, "".join([f.capitalize() for f in filteredData]), matches1[0]).ratio()
			all.append((matches1[0], simScore))
	return all
def conjectTextInRegion(original:cv2.Mat, region:CropBox, options:list[str], chunkSizes:list[int]=[150, 300]) -> tuple[str,float]|None:
	"""Reads the text in given reagion with tesseract and compares found results to a list of valid options

	Args:
		original (cv2.Mat): Target image
		region (CropBox): Region to read from
		options (list[str]): Valid options
		chunkSizes (list[int], optional): List of chunksizes for fallback function. Defaults to [150, 300].

	Returns:
		tuple[str,float]|None: The found text (text, confidence); null if the confidence was not above threshold
	"""
	cropped:cv2.Mat = region.crop(original)
	croppedArea:int = cropped.shape[0]*cropped.shape[1]
	gray:cv2.Mat = toGrayscale(cropped)
	thresh:cv2.Mat = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)[1] # type: ignore
	labels, stats = cv2.connectedComponentsWithStats(thresh)[1:3]
	for label in range(1, labels.max()):
		area = stats[label,cv2.CC_STAT_AREA]
		if area < croppedArea*.002 or area > croppedArea*.04: labels[labels==label] = 0 # .001, .035
	threshed = cv2.bitwise_and(gray, gray, mask=(labels>0).astype(np.uint8))
	read:dict[str,list[str]] = pytesseract.image_to_data(threshed, config=tess_config, output_type=pytesseract.Output.DICT) # type: ignore
	filteredData:list[str] = []	
	for r in read["text"]:
		if len(r) > 1: filteredData.append(r)
	# Image.fromarray(threshed).save(f"./preprocessed/{'_'.join(options)}.png")
	matches1:list[str] = difflib.get_close_matches("".join([f.capitalize() for f in filteredData]), options, n=1000, cutoff=.65) # .58
	if len(matches1) > 0:
		simScore:float = difflib.SequenceMatcher(None, "".join([f.capitalize() for f in filteredData]), matches1[0]).ratio()
		return (matches1[0], simScore)
	for cs in chunkSizes:
		res:list[tuple[str, float]] = conjectTextInRegionChunked(original, region, options, cs)
		if len(res) > 0:
			return res[0]
	return None

def load(opId:str) -> Operator:
	"""Loads the Operator object from file

	Args:
		opId (str): Operator id

	Returns:
		Operator: Deserialized Operator object
	"""
	op:Operator = pickle.load(open(f"./userdata/saves/{opId}.spec", "rb"))
	op.recreateImg()
	return op