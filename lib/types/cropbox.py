import cv2
import math

class CropBox:
	"""Cropbox to crop a cv2.Mat image

	Attributes:
		x (int): x location
		x (int): y location
		w (int): Width to crop
		h (int): Height to crop
		tolerance (int): Will extend the cropped image by n pixels to each side
	"""
	def __init__(self, x:int, y:int, w:int, h:int, tolerance:int=0) -> None:
		"""Constructor of CropBox

		Args:
			x (int): x location
			y (int): y location
			w (int): Width to crop
			h (int): Height to crop
			tolerance (int, optional): Will extend the cropped image by n pixels to each side. Defaults to 0.
		"""
		self.x:int = int(x)
		self.y:int = int(y)
		self.w:int = int(w)
		self.h:int = int(h)
		self.tolerance:int = int(tolerance)
	def toTuple(self) -> tuple[int,...]:
		"""Converts the position values to a tuple

		Returns:
			tuple[int,...]: (x, y, w, h)
		"""
		return (self.x, self.y, self.w, self.h)
	def crop(self, img:cv2.Mat) -> cv2.Mat:
		"""Crops the image

		Args:
			img (cv2.Mat): The image to crop

		Returns:
			cv2.Mat: Cropped image extended by tolerance
		"""
		return img[self.y-self.tolerance:self.y+self.h+self.tolerance, self.x-self.tolerance:self.x+self.w+self.tolerance]
	def split(self, width:int) -> list[tuple[int,...]]:
		"""Splits the CropBox into multiple chunks with given width

		Args:
			width (int): Width of the chunks

		Returns:
			list[tuple[int,...]]: List of the splitted CropBox
		"""
		return [(self.x+int(width)*i, self.y, int(width), self.h) for i in range(math.ceil(self.w/width))]
	def cropSplit(self, img:cv2.Mat, width:int) -> list[cv2.Mat]:
		"""Combines crop and split

		Args:
			img (cv2.Mat): Image to crop
			width (int): Chunk width

		Returns:
			list[cv2.Mat]: List of cropped images
		"""
		return [CropBox(*i, tolerance=self.tolerance).crop(img) for i in self.split(width)]
	def add(self, pos:list[tuple[int,...]]) -> tuple[int,...]:
		"""adds the x and y coordinates of two CropBoxes

		Args:
			pos (list[tuple[int,...]]): CropBox position as tuple

		Returns:
			tuple[int,...]: New position data
		"""
		# if type(pos) == list:
		xT:int = self.x
		yT:int = self.y
		for p in pos:
			xT += p[0]
			yT += p[1]
		return (xT, yT, self.w, self.h)
		# return (self.x+pos[0],self.y+pos[1],self.w,self.h)

	def __str__(self) -> str:
		return f"<{type(self).__name__} x={self.x}, y={self.y}, w={self.w}, h={self.h}, tolerance={self.tolerance}>"

class Circle:
	"""Circle to crop a cv2.Mat image

	Attributes:
		x (int): x location
		x (int): y location
		r (int): Radius to crop
	"""
	def __init__(self, x:int, y:int, r:int) -> None:
		self.x:int = x
		self.y:int = y
		self.r:int = r
	def toTuple(self) -> tuple[int,...]:
		"""Converts the position values to a tuple

		Returns:
			tuple[int,...]: (x, y, r)
		"""
		return (self.x, self.y, self.r)
	def getBoundingBox(self) -> CropBox:
		"""Returns a CropBox sorounding the circle

		Returns:
			CropBox: Bounding CropBox
		"""
		return CropBox(self.x-self.r, self.y-self.r, 2*self.r, 2*self.r)
	def crop(self, img:cv2.Mat) -> cv2.Mat:
		"""Crops the target image by the CropBox sorounding the circle

		Args:
			img (cv2.Mat): Target image

		Returns:
			cv2.Mat: Cropped image
		"""
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