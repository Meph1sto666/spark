from lib.types.misc import *
from lib.types.errors import *
from lib.types.cropbox import *
import numpy as np
import pytesseract # type: ignore
import cv2

class Module:
	def __init__(self, img:cv2.Mat, opId:str, opProm:int, stageCropBox:CropBox, typeCropBox:CropBox) -> None:
		self.tTracker:TimeTracker = TimeTracker(dt.now())
		self.OP_ID:str = opId
		self.stageCropBox:CropBox = stageCropBox
		self.typeCropBox:CropBox = typeCropBox

		self.moduleOptions:list[dict[str,str]] = dict(json.load(open("./ref/operators.json"))).get(opId,{}).get("modules", []) if opProm > 1 else []
		self.stage:int|None = None
		self.type:str|None = None
		self.foundTypeCropBox:CropBox|None = None
		# self.foundStateCropBox:CropBox|None
		if len(self.moduleOptions) > 0:
			self.stage = self.conjectModuleStage(img)
			self.tTracker.add(Delta(dt.now(), "stage"))
			if self.stage != None:
				if len(self.moduleOptions) == 1:
					self.type = self.moduleOptions[0].get("typeName")
				else:
					self.type = self.conjectModuleType(img)
				self.tTracker.add(Delta(dt.now(), "type"))
				
			
	def conjectModuleStage(self, img:cv2.Mat) -> int | None:
		stageImg:cv2.Mat = self.stageCropBox.crop(img)
		stageThresh:cv2.Mat = cv2.threshold(stageImg, 100, 255, cv2.THRESH_BINARY)[1] # type: ignore
		data:dict[str, list[str]] = pytesseract.image_to_data(stageThresh, config="--psm 10 --oem 3 -c tessedit_char_whitelist=123", output_type=pytesseract.Output.DICT) # type: ignore
		filtered:list[str] = list(filter(lambda x: 0 < len(x) < 2, data["text"]))
		return int(filtered[0]) if len(filtered) > 0 else None

	def conjectModuleType(self, img:cv2.Mat) -> str | None:
		cropped:cv2.Mat = self.typeCropBox.crop(img)
		imgThresh:cv2.Mat = cv2.threshold(toGrayscale(cropped), 130, 255, cv2.THRESH_BINARY)[1] # type: ignore
		data:list[tuple[float,str,CropBox]] = []
		streak:int = 0
		for e in [m.get("typeName", "").lower() for m in self.moduleOptions]:
			refImg:cv2.Mat = cv2.imread(f"./ref/equip/{e}.png", cv2.IMREAD_UNCHANGED)
			refGray:cv2.Mat = toGrayscale(refImg)
			refThresh:cv2.Mat = cv2.threshold(refGray, 130, 255, cv2.THRESH_BINARY)[1] # type: ignore
			refMasked:cv2.Mat = cv2.bitwise_and(refThresh, refThresh, mask=refImg[:,:,3])
			for s in range(int(self.typeCropBox.w/2), self.typeCropBox.w):
				if len(data) > 0 and streak < 0: break
				refResized:cv2.Mat = cv2.resize(refMasked, (s,s))
				res:cv2.Mat = cv2.matchTemplate(imgThresh, refResized, cv2.TM_CCOEFF_NORMED)
				loc:tuple[cv2.Mat,...] = np.where(res >= .75) # type: ignore
				if len(loc[0]) > 0:
					pos:list[tuple[int,...]] = list(zip(*loc[::-1]))
					data.append((float(np.max(res)), e, CropBox(pos[0][0], pos[0][1], refResized.shape[1], refResized.shape[0]))) # type: ignore
					streak = len(self.moduleOptions)+1
				else: streak-=1
		srt:tuple[float, str, CropBox] = sorted(data, key=lambda x: -x[0])[0]
		if not len(srt) > 0: return None
		self.foundTypeCropBox = srt[2]
		return srt[1]