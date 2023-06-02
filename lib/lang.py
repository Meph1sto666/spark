import json
import os
# LANG_FOLDER:str = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data/lang/"
LANG_FOLDER:str = "./data/lang/"
LANG_FILE_EXT = ".json"

class Lang:
	def __init__(self, l:str="en_us") -> None:
		self.name:str = l
		self.langData:dict[str, str] = json.load(open(LANG_FOLDER + self.name + LANG_FILE_EXT, "r", encoding="utf-8"))
	
	def __str__(self) -> str:
		return self.name
	
	def loadLanguage(self, lName:str) -> None:
		"""Loads a language

		Args:
			lName (str): language file name
		"""
		try:
			self.langData = json.load(open(LANG_FOLDER + lName + LANG_FILE_EXT, "r", encoding="utf-8"))
			self.name = lName
		except: pass

	def translate(self, key:str, translation:int=0) -> str:
		"""Translates the given key to the target language

		Args:
			key (str): Dictionary key for translation
			translation (int, optional): If multiple possible translations exist choose one of them. Defaults to 0.

		Returns:
			str: The translation or an error string eg. <en_us.test_key> (target langauge.not existing key)
		"""
		# return self.langData.get(key, f"<{self.name}.{key}>") if type(self.langData.get(key, []))== list and len(self.langData.get(key, [])) < 2 else self.langData.get(key)[translation]
		if type(self.langData.get(key, None)) == list:
			try:
				return self.langData.get(key, [])[translation]
			except:
				return f"<{self.name}.{key}[{translation}]>"
		return self.langData.get(key, f"<{self.name}.{key}>")

def getAvialLangs() -> list[str]:
	"""Returns all aviable language files from the ./data/lang/ folder

	Returns:
		list[str]: List of aviable languages
	"""
	return [i.removesuffix(LANG_FILE_EXT) for i in list(filter(lambda l: l.endswith(LANG_FILE_EXT), os.listdir(LANG_FOLDER)))]