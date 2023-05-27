import cv2
from lib.types.misc import *
import numpy as np
import pytesseract
from lib.types.cropbox import *

img:cv2.Mat = cv2.imread(f"./testdata/9.png", cv2.IMREAD_UNCHANGED)
def conjectModuleStage(original:cv2.Mat) -> int | None:
	stageImg:cv2.Mat = original[750:-250, 1500:-1]
	stageThresh:cv2.Mat = cv2.threshold(stageImg, 100, 255, cv2.THRESH_BINARY)[1] # type: ignore
	data:dict[str, list[str]] = pytesseract.image_to_data(stageThresh, config="--psm 10 --oem 3 -c tessedit_char_whitelist=123", output_type=pytesseract.Output.DICT) # type: ignore
	filtered:list[str] = list(filter(lambda x: 0 < len(x) < 2, data["text"]))
	return int(filtered[0]) if len(filtered) > 0 else None

# --------------------

def conjectModuleTyp(original:cv2.Mat) -> str | None:
	cropped:cv2.Mat = original[700:-200,1400:-150]
	imgThresh:cv2.Mat = cv2.threshold(toGrayscale(cropped), 100, 255, cv2.THRESH_BINARY)[1] # type: ignore
	data:list[tuple[float,int,CropBox]] = []
	streak = 0
	for e in os.listdir("./ref/equip/"): # NOTE: replace with only the modules the op has
		refImg:cv2.Mat = cv2.imread(f"./ref/equip/{e}", cv2.IMREAD_UNCHANGED)
		refGray:cv2.Mat = toGrayscale(refImg)
		refMasked:cv2.Mat = cv2.bitwise_and(refGray, refGray, mask=refImg[:,:,3])
		for s in range(75, 100):
			if len(data) > 0 and streak < 0: break
			refResized:cv2.Mat = cv2.resize(refMasked, (s,s))
			res:cv2.Mat = cv2.matchTemplate(imgThresh, refResized, cv2.TM_CCOEFF_NORMED)
			loc:tuple[cv2.Mat,...] = np.where(res >= .75) # type: ignore
			if len(loc[0]) > 0:
				pos:list[tuple[int,...]] = list(zip(*loc[::-1]))
				data.append((float(np.max(res)), os.path.splitext(e)[0], CropBox(pos[0][0], pos[0][1], refResized.shape[1], refResized.shape[0]))) # type: ignore
				streak = 7
			else: streak-=1
	srt:tuple[float, int, CropBox] = sorted(data, key=lambda x: -x[0])[0]
	if len(srt) > 0: return srt[0]

print(conjectModuleTyp(img))