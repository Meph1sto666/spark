from lib.types.misc import *
from lib.types.errors import *
from lib.types.cropbox import *
import numpy as np
import cv2
# from PIL import Image

class Skill:
	"""Skill class (does not have an index for the skill)

	Atributes:
		skillCropBox (CropBox): Skill position
		masteryCropBox (CropBox|None): If the skill has a mastery level 1, 2, 3 not null
		mastery (int): The skill's mastery level
	"""
	def __init__(self, img:cv2.Mat, box:CropBox) -> None:
		"""Constructor of Skill

		Args:
			img (cv2.Mat): Target image
			box (CropBox): position of the skill within image
		"""
		self.skillCropBox:CropBox = box
		self.masteryCropBox:CropBox|None = None
		self.mastery:int = self.conjectSkillMasteryLevel(img)

	def conjectSkillMasteryLevel(self, img:cv2.Mat) -> int:
		"""Conjecting operator skill masteries with template matching

		Args:
			img (cv2.Mat): Target image

		Returns:
			int: Mastery level of the skill
		"""
		cropped:cv2.Mat = self.skillCropBox.crop(img)
		imgGray:cv2.Mat = toGrayscale(cropped)
		imgThresh:cv2.Mat = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY)[1] # type: ignore
		data:list[tuple[float,int,CropBox]] = []
		streak = 0
		files:list[str] = os.listdir("./ref/mastery/")
		for m in files:
			refImg:cv2.Mat = cv2.imread(f"./ref/mastery/{m}")
			refGray:cv2.Mat = toGrayscale(refImg)
			for s in range(int(self.skillCropBox.w/2), int(self.skillCropBox.w)):
				refResized:cv2.Mat = cv2.resize(refGray, (s,s))
				res:cv2.Mat = cv2.matchTemplate(imgThresh, refResized, cv2.TM_CCOEFF_NORMED)
				loc:tuple[cv2.Mat, ...] = np.where(res >= .8) # type: ignore
				if len(loc[0]) > 0:
					pos:list[tuple[int,...]] = list(zip(*loc[::-1]))
					data.append((float(np.max(res)), int(os.path.splitext(m)[0]), CropBox(pos[0][0], pos[0][1], refResized.shape[1], refResized.shape[0]))) # type: ignore
					streak:int = len(files)-1
				else: streak-=1
		if not len(data) > 0: return 0
		srt:tuple[float, int, CropBox] = sorted(data, key=lambda x: -x[0])[0]
		self.masteryCropBox = srt[2]
		return srt[1]

class Skills:
	def __init__(self, img:cv2.Mat, promAnchor:RefData, rarity:int) -> None:
		self.sb:CropBox = self.getRankPos(promAnchor, img)
		self.rank:int = self.conjectSkillRank(img)
		self.masteries:list[Skill|None] = []

		amount = 0
		if rarity > 5: amount:int = 3 
		elif rarity > 3: amount = 2
		elif rarity > 2: amount = 1
		if self.rank == 7:
			for s in range(amount):
				skill = Skill(img, self.getMasteriesPos(promAnchor,img,s))
				self.masteries.append(skill)
				# Image.fromarray(skill.skillCropBox.crop(img)).save(f"./preprocessed/preprocess_skill_{s}.png","png")
			# self.masteries = [Skill(img, self.getMasteriesPos(promAnchor,img,s)) for s in range(amount)]

	def conjectSkillRank(self, img:cv2.Mat) -> int:
		"""Conjecting operator skill level with template matching

		Args:
			img (cv2.Mat): Target image

		Raises:
			SkillRankConjectionFailed: When the skill rank could not be recognised

		Returns:
			int: Skill rank
		"""
		cropped:cv2.Mat = self.sb.crop(img)
		imgGray:cv2.Mat = toGrayscale(cropped)
		# Image.fromarray(imgGray).save(f"./preprocessed/preprocess_skill_rank.png","png")
		data:list[tuple[float,int,CropBox]] = []
		streak = 0
		for m in os.listdir("./ref/rank/"):
			refImg:cv2.Mat = cv2.imread(f"./ref/rank/{m}", cv2.IMREAD_UNCHANGED)
			refGray:cv2.Mat = toGrayscale(refImg)
			refMasked:cv2.Mat = cv2.bitwise_and(refGray, refGray, mask=refImg[:,:,3])
			for s in range(int(self.sb.h*.9), int(self.sb.h)):
				refResized:cv2.Mat = cv2.resize(refMasked, (s,s))
				res:cv2.Mat = cv2.matchTemplate(imgGray, refResized, cv2.TM_CCOEFF_NORMED)
				loc:tuple[cv2.Mat, ...] = np.where(res >= .7) # type: ignore
				if len(loc[0]) > 0:
					pos:list[tuple[int,...]] = list(zip(*loc[::-1]))
					data.append((float(np.max(res)), int(os.path.splitext(m)[0]), CropBox(pos[0][0], pos[0][1], refResized.shape[1], refResized.shape[0]))) # type: ignore
					streak = 2
				else: streak-=1
		if len(data) > 0:
			srt:tuple[float, int, CropBox] = sorted(data, key=lambda x: -x[0])[0]
			self.masteryCropBox:CropBox = srt[2]
			return srt[1]
		raise SkillRankConjectionFailed()

	def isMasteryable(self) -> bool:
		"""Determins if the operators skills are masteryable (true if operator rarity > 3)

		Returns:
			bool: True if Op can have masteries
		"""
		return self.rank > 6

	def getRankPos(self, anchor:RefData, img:cv2.Mat) -> CropBox:
		"""Returns the position of the skill rank

		Args:
			anchor (RefData): Promotion anchor
			img (cv2.Mat): The target image

		Returns:
			CropBox: Position of the rank
		"""
		return CropBox(
			x=int(anchor.x*1.38),
			y=int((anchor.y-(img.shape[0]-img.shape[1]/(16/9))/4)*1.75),
			w=int(anchor.size*.4),
			h=int(anchor.size*.28),
			tolerance=0 # NOTE: maybe 5
		)

	def getMasteriesPos(self, anchor:RefData, img:cv2.Mat, i:int) -> CropBox:
		"""Returns the position of the mastery given by it's number 0 - 2

		Args:
			anchor (RefData): Promotion anchor
			img (cv2.Mat): The target image
			i (int): index of the mastery

		Returns:
			CropBox: Position of the value
		"""
		return CropBox(
			x=int(anchor.x+anchor.size*i*.925),
			y=int((anchor.y-(img.shape[0]-img.shape[1]/(16/9))/4)*1.625),
			w=int(anchor.size*.35), # w = h to prevent errors
			h=int(anchor.size*.35), # w = h to prevent errors
			tolerance=0
		)