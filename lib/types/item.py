import cv2
import pytesseract
from lib.types.cropbox import *
from lib.types.errors import *
from lib.types.misc import *
from PIL import Image # type: ignore
import numpy as np

class Item:
	def __init__(self, img:cv2.Mat, pos:CropBox) -> None:
		self.cropbox:CropBox = pos
		self.ORIGINAL:cv2.Mat = pos.crop(img)
		# print(self.conjectAmount())
	
	def conjectAmount(self) -> int:
		# thresh = toGrayscale(cv2.threshold(self.ORIGINAL[int(self.ORIGINAL.shape[0]/4):,int(self.ORIGINAL.shape[1]/4):], 100, 255, cv2.THRESH_BINARY)[1])

		cropped:cv2.Mat = self.ORIGINAL[int(self.ORIGINAL.shape[0]/4):,int(self.ORIGINAL.shape[1]/4):]
		mask:cv2.Mat = toGrayscale(cv2.threshold(cropped, 200, 255, cv2.THRESH_BINARY)[1]) # type: ignore / create mask from cropped image
		kernel:cv2.Mat = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(mask.shape[0]/10),int(mask.shape[1]/10))) # type: ignore
		mask2:cv2.Mat = cv2.bitwise_not(cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)) # type: ignore
		croppedMasked:cv2.Mat = cv2.bitwise_and(cropped, cropped, mask=cv2.bitwise_and(mask,mask2)) # mask the cropped Image
		# Image.fromarray(croppedMasked).show()

		dta = pytesseract.image_to_data(toGrayscale(croppedMasked), config="--psm 10 --oem 3 -c tessedit_char_whitelist=1234567890K.", output_type=pytesseract.Output.DICT) # type: ignore
		# print(dta["text"])
		return(dta["text"]) # type: ignore



def locateItems(img:cv2.Mat) -> list[Circle]:
	circles = cv2.HoughCircles(toGrayscale(img), cv2.HOUGH_GRADIENT, 1, 25, param1=1, param2=50,minRadius=80,maxRadius=105) # type: ignore
	return [Circle(*c) for c in np.round(circles[0,])] # type: ignore