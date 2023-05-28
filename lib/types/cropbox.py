import cv2
import math

class CropBox:
	def __init__(self, x:int, y:int, w:int, h:int, tolerance:int=0) -> None:
		self.x:int = int(x)
		self.y:int = int(y)
		self.w:int = int(w)
		self.h:int = int(h)
		self.tolerance:int = int(tolerance)
	def toTuple(self) -> tuple[int,...]:
		return (self.x, self.y, self.w, self.h)
	def crop(self, img:cv2.Mat) -> cv2.Mat:
		return img[self.y-self.tolerance:self.y+self.h+self.tolerance, self.x-self.tolerance:self.x+self.w+self.tolerance]
	def split(self, width:int) -> list[tuple[int,...]]:
		return [(self.x+int(width)*i, self.y, int(width), self.h) for i in range(math.ceil(self.w/width))]
	def cropSplit(self, img:cv2.Mat, width:int) -> list[cv2.Mat]:
		return [CropBox(*i, tolerance=self.tolerance).crop(img) for i in self.split(width)]
	def add(self, pos:list[tuple[int,...]]) -> tuple[int,...]:
		# if type(pos) == list:
		xT:int = self.x
		yT:int = self.y
		for p in pos:
			xT += p[0]
			yT += p[1]
		return (xT, yT, self.w, self.h)
		# return (self.x+pos[0],self.y+pos[1],self.w,self.h)

class Circle:
	def __init__(self, x:int, y:int, r:int) -> None:
		self.x:int = x
		self.y:int = y
		self.r:int = r
	def toTuple(self) -> tuple[int,...]:
		return (self.x, self.y, self.r)
	def getBoundingBox(self) -> CropBox:
		return CropBox(self.x-self.r, self.y-self.r, 2*self.r, 2*self.r)
	def crop(self, img:cv2.Mat) -> cv2.Mat:
		return self.getBoundingBox().crop(img)

class SkillBox(CropBox):
	def __init__(self, x: int, y: int, w: int, h: int, tolerance: int = 0) -> None:
		super().__init__(x, y, w, h, tolerance)
		self.rankWidth:int = math.ceil(w*(4/15))
		self.skillWidth:int = math.ceil((w-self.rankWidth) / 3)

	def cropSkill(self, img:cv2.Mat, skillNum:int) -> cv2.Mat:
		return img[self.y-self.tolerance:self.y+self.h+self.tolerance,
			self.x-self.tolerance+(skillNum*self.skillWidth):self.x+self.tolerance+((skillNum+1)*self.skillWidth)]
	def cropSkills(self, img:cv2.Mat) -> list[cv2.Mat]:
		return [
				img[self.y-self.tolerance:self.y+self.h+self.tolerance, self.x-self.tolerance+(s*self.skillWidth):self.x+self.tolerance+((s+1)*self.skillWidth)]
				for s in range(3)
			]

	def getSkillCropBoxes(self, amount:int=3) -> list[CropBox]:
		return [
				CropBox(
					x=self.x+(s*self.skillWidth),
					y=self.y,
					w=self.skillWidth,
					h=self.h
				)
				for s in range(amount)
			]

	def cropRank(self, img:cv2.Mat) -> cv2.Mat:
		return img[self.y-self.tolerance:self.y+self.h+self.tolerance, self.x-self.tolerance+self.w-self.rankWidth:self.x+self.tolerance+self.w]