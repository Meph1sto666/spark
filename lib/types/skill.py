from lib.types.misc import *
from lib.types.errors import *
from lib.types.cropbox import *
import numpy as np
import pytesseract # type: ignore
import cv2
from PIL import Image

class Skill:
	def __init__(self, img:cv2.Mat, box:CropBox) -> None:
		self.ORIGINAL:cv2.Mat = img
		self.skillCropBox:CropBox = box
		self.masteryCropBox:CropBox|None = None
		self.mastery:int = self.conjectSkillMasteryLevel()
		# self.selected:bool = self.conjectSkillSelection()

	def conjectSkillMasteryLevel(self) -> int:
		cropped:cv2.Mat = self.skillCropBox.crop(self.ORIGINAL)
		imgGray:cv2.Mat = toGrayscale(cropped)
		imgThresh:cv2.Mat = cv2.threshold(imgGray, 150, 255, cv2.THRESH_BINARY)[1] # type: ignore
		data:list[tuple[float,int,CropBox]] = []
		streak = 0
		for m in os.listdir("./ref/mastery/"):
			refImg:cv2.Mat = cv2.imread(f"./ref/mastery/{m}")
			refGray:cv2.Mat = toGrayscale(refImg)
			for s in range(int(self.skillCropBox.w/5)-5, int(self.skillCropBox.w/5)+5):
				refResized:cv2.Mat = cv2.resize(refGray, (s,s))
				res:cv2.Mat = cv2.matchTemplate(imgThresh, refResized, cv2.TM_CCOEFF_NORMED)
				loc:tuple[cv2.Mat, ...] = np.where(res >= .8) # type: ignore
				if len(loc[0]) > 0:
					pos:list[tuple[int,...]] = list(zip(*loc[::-1]))
					data.append((float(np.max(res)), int(os.path.splitext(m)[0]), CropBox(pos[0][0], pos[0][1], refResized.shape[1], refResized.shape[0]))) # type: ignore
					streak = 7
				else: streak-=1
		if not len(data) > 0: return 0
		srt:tuple[float, int, CropBox] = sorted(data, key=lambda x: -x[0])[0]
		self.masteryCropBox = srt[2]
		return srt[1]

	# def conjectSkillSelection(self) -> bool:
	# 	cropped:cv2.Mat = self.skillCropBox.crop(self.ORIGINAL)
	# 	rgMask:cv2.Mat = cv2.bitwise_not(*cv2.split(cropped)[1:3])
	# 	imgMasked:cv2.Mat = cv2.bitwise_and(cropped,cropped, mask=rgMask)
	# 	imgGray:cv2.Mat = cv2.split(imgMasked)[0]
	# 	imgThresh:cv2.Mat = cv2.threshold(imgGray, 200, 255, cv2.THRESH_BINARY)[1] # type: ignore
	# 	# Image.fromarray(imgThresh).show()
	# 	contours = cv2.findContours(imgThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
	# 	filtered = list(filter(lambda c: cv2.contourArea(c) > 100, contours))
	# 	print(len(contours))
	# 	for c in filtered:
	# 		# approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c, True), True)
	# 		# if len(approx) == 3:
	# 		drawBoundingBox(cropped, *cv2.boundingRect(c))
	# 	if len(filtered) >0:
	# 		Image.fromarray(cropped).show()
	# 	return False

class Skills:
	def __init__(self, img:cv2.Mat, skillBox:SkillBox) -> None:
		self.ORIGINAL:cv2.Mat = img
		self.sb:SkillBox = skillBox
		self.rank:int = self.conjectSkillRank()
		self.masteries:list[Skill|None] = [None, None, None]
		if self.rank == 7:
			self.masteries = [Skill(self.ORIGINAL, s) for s in skillBox.getSkillCropBoxes()]

	def conjectSkillRank(self) -> int:
		cropped:cv2.Mat = self.sb.cropRank(self.ORIGINAL)
		letters:list[CropBox] = findLetters(cropped)
		# cropped = cropped[25:cropped.shape[0]-25, 75:]
		gray:cv2.Mat = toGrayscale(cropped)
		for l in letters:
			lttr:cv2.Mat = l.crop(gray)
			threshed:cv2.Mat = cv2.threshold(lttr, 200, 255, cv2.THRESH_BINARY)[1] # type: ignore
			data:dict[str, list[str|int]] = pytesseract.image_to_data(threshed, config="--psm 10 --oem 3 -c tessedit_char_whitelist=1234567", output_type=pytesseract.Output.DICT) # type: ignore
			filtered:list[str | int] = list(filter(lambda x: len(str(x)) == 1, data["text"]))
			if len(filtered) > 0:
				Image.fromarray(lttr).show()
				return int(filtered[0])
			

		
		raise SkillRankConjectionFailed()
