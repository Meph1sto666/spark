import json
SETTINGS_FILE:str = "./userdata/settings.json"

def getBool(setting:str) -> bool:
	return bool(json.load(open(SETTINGS_FILE))[setting])
def setBool(setting:str, state:bool) -> None:
	json.load(open(SETTINGS_FILE))[setting] = bool(state)

def getString(setting:str) -> str:
	return str(json.load(open(SETTINGS_FILE))[setting])
def setString(setting:str, value:str) -> None:
	json.load(open(SETTINGS_FILE))[setting] = str(value)

def getNum(setting:str) -> float:
	return float(json.load(open(SETTINGS_FILE))[setting])
def setNum(setting:str, value:float) -> None:
	json.load(open(SETTINGS_FILE))[setting] = float(value)
