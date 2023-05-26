from lib.types.misc import *
from lib.types.errors import *
from lib.types.cropbox import *
import numpy as np
import pytesseract # type: ignore
import cv2
from PIL import Image



class SkillMastery:
	def __init__(self, img:cv2.Mat, box:CropBox) -> None:
		self.ORIGINAL:cv2.Mat = img
		self.skillCropBox:CropBox = box
		# print("cropped Skill shape", self.ORIGINAL.shape)
		# print("cropbox size", self.skillCropBox.toTuple())
		self.circlesCropBox:list[Circle] = []
		self.mastery:int = self.conjectSkillMasteryLevel()
		print(self.mastery)
	"""
	def conjectSkillMasteryLevel(self) -> int:
		cropped:cv2.Mat = self.skillCropBox.crop(self.ORIGINAL)
		cropped:cv2.Mat = cropped[0:int(cropped.shape[0]*.4),0:int(cropped.shape[1]*.4)]
		# Image.fromarray(cropped).show()
		threshed:cv2.Mat = cv2.threshold(cropped, 250, 255, cv2.THRESH_BINARY)[1] # type: ignore
		# Image.fromarray(threshed).show()
		shapes:list[list[tuple[int,...]]] = cv2.findContours(toGrayscale(threshed), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] # type: ignore
		circles:list[tuple[int,...]] = []
		for s in shapes:
			if cv2.contourArea(s) < 10: continue # type: ignore
			if cv2.contourArea(s) > 20: continue # type: ignore
			circles.append(s) # type: ignore
		for circle in circles:
			self.circlesCropBox.append(CropBox(*cv2.boundingRect(circle))) # type: ignore
		
		for c in self.circlesCropBox:
			drawBoundingBox(cropped, *(c.toTuple()), text=str(len(circles)))
			Image.fromarray(cropped).show()
		return len(circles)
		# raise SkillMasteryConjectionFailed()	"""
	def conjectSkillMasteryLevel(self) -> int | None:
		cropped:cv2.Mat = self.skillCropBox.crop(self.ORIGINAL)
		cropped:cv2.Mat = cropped[0:int(cropped.shape[0]*.35),0:int(cropped.shape[1]*.3)]
		Image.fromarray(cropped).show()
		threshed:cv2.Mat = cv2.threshold(cropped, 250, 255, cv2.THRESH_BINARY)[1] # type: ignore
		# Image.fromarray(threshed).show()

		circles = cv2.HoughCircles(toGrayscale(threshed), cv2.HOUGH_GRADIENT, dp=1, minDist=5, param1=1, param2=5, minRadius=2, maxRadius=10)
		if circles is None: return None
		for (x, y, r) in np.round(circles[0, :]).astype("int"): # type: ignore
			# cv2.circle(cropped, (x, y), r, (0, 255, 0), 2) # type: ignore
			self.circlesCropBox.append(Circle(x,y,r)) # type: ignore
		
		for c in self.circlesCropBox:
			drawBoundingBox(cropped, *(c.getBoundingBox().toTuple()), text=str(len(circles)))
		Image.fromarray(cropped).show() # type: ignore
		return len(self.circlesCropBox)
		# raise SkillMasteryConjectionFailed()

class Skills:
	def __init__(self, img:cv2.Mat, skillBox:SkillBox) -> None:
		self.ORIGINAL:cv2.Mat = img
		self.sb:SkillBox = skillBox
		self.rank:int = self.conjectSkillRank()
		self.masteries:list[SkillMastery|None] = [None, None, None]
		if self.rank == 7:
			self.masteries = [SkillMastery(self.ORIGINAL, s) for s in skillBox.getSkillCropBoxes()]
			print(m.mastery for m in self.masteries)
  
	def conjectSkillRank(self) -> int:
		cropped:cv2.Mat = self.sb.cropRank(self.ORIGINAL)
		cropped = cropped[25:cropped.shape[0]-25, 75:]
		threshed:cv2.Mat = cv2.threshold(cropped, 100, 255, cv2.THRESH_BINARY)[1] # type: ignore
		# Image.fromarray(threshed).show()
		data:dict[str, list[str|int]] = pytesseract.image_to_data(threshed, config="--psm 10 --oem 3 -c tessedit_char_whitelist=1234567", output_type=pytesseract.Output.DICT) # type: ignore
		filtered:list[str | int] = list(filter(lambda x: len(str(x)) == 1, data["text"]))
		# print(data["text"])
		if len(filtered) > 0:
			return int(filtered[0])
		raise SkillRankConjectionFailed()